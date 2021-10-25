# -*- coding: utf-8 -*-
import inspect
import os
from importlib import import_module
from sys import prefix
from typing import Optional
from somali.apis import Twitch, twitch
from somali.database.models.user import User as UserPrefix


from twitchio.ext.commands import (
    Bot,
    Bucket,
    Command,
    Context,
    Cooldown,
)
from twitchio.ext.commands.errors import (
    CheckFailure,
    CommandNotFound,
    CommandOnCooldown,
    MissingRequiredArgument,
)
from twitchio.ext.routines import Routine
from twitchio.message import Message

from somali import log
from somali.apis import AI, Analytics
from somali.database.models import Channel, User
from somali.exceptions import (
    BotIsOffline,
    CommandIsDisabled,
    ContentHasBanword,
    GameIsAlreadyRunning,
    InvalidName,
    UserIsNotAllowed,
)
from somali.utils import checks

DEFAULT_COOLDOWN_RATE = 2
DEFAULT_COOLDOWN_PER = 2
DEFAULT_COOLDOWN_BUCKET = Bucket.user



class Ctx(Context):
    def __init__(self, message: Message, bot: Bot, **kwargs) -> None:
        super().__init__(message, bot, **kwargs)
        self.response: Optional[str] = None
        self.prediction: dict = {}
        self.user: User = None

    def __iter__(self):
        yield "author", getattr(self.author, "id", None)
        yield "channel", getattr(self.channel, "id", None)
        yield "user", getattr(self.user, "id", None)
        yield "message", getattr(self.message, "content", None)
        yield "response", self.response


class TwitchBot(Bot):
    def __init__(self, config):
        super().__init__(
            token=config.access_token,
            client_secret=config.client_secret,
            prefix = config.prefix,
            case_insensitive=True,
        )
        self.mentions: bool = config.ai_url and config.ai_key
        self.owner: str = config.owner
        self.site: str = config.site_url
        self.blocked: list = []
        self.listeners: list = []
        self.routines: list = []
        self.channels: dict = {}
        self.cache: object = None
        # self._prefix: list = prefiquixi

    
    async def start(self) -> None:
        await self.connect()
        await self.add_all_channels()
        await self.fetch_blocked()

    async def stop(self) -> None:
        [routine.stop() for routine in self.routines]
        await self.close()

    async def adiciona(self):
        await self.add_all_channels()

    def add_checks(self) -> None:
        for check in [checks.online, checks.enabled, checks.banword]:
            self.check(check)

    def load_commands(self, path: str) -> None:
        for filename in os.listdir(path):
            if not filename.endswith(".py") or filename.startswith("__"):
                continue
            try:
                local: str = os.path.join(path, filename)
                name: str = local[:-3].replace("/", ".")
                package: str = path.replace("/", ".")
                module: types.ModuleType = import_module(name, package=package)
                cooldown: dict = getattr(module, "cooldown", {})
                module.command.__cooldowns__: list = [
                    Cooldown(
                        cooldown.get("rate", DEFAULT_COOLDOWN_RATE),
                        cooldown.get("per", DEFAULT_COOLDOWN_PER),
                        cooldown.get("bucket", DEFAULT_COOLDOWN_BUCKET),
                    )
                ]
                module.command.__checks__: list = getattr(module, "extra_checks", [])
                command: Command = Command(
                    name=getattr(module, "name", filename[:-3]),
                    func=module.command,
                    aliases=getattr(module, "aliases", None),
                    no_global_checks=getattr(module, "no_global_checks", False),
                )
                command.description: str = module.description
                command.usage: Optional[str] = getattr(module, "usage", None)
                self.add_command(command)
            except Exception as e:
                log.error(f"Command '{filename[:-3]}' failed to load: {e}", extra={"locals": locals()})

    def load_listeners(self, path: str) -> None:
        for filename in os.listdir(path):
            if not filename.endswith(".py") or filename.startswith("__"):
                continue
            try:
                local: str = os.path.join(path, filename)
                name: str = local[:-3].replace("/", ".")
                package: str = path.replace("/", ".")
                module: types.ModuleType = import_module(name, package=package)
                self.listeners.append(module.listener)
            except Exception as e:
                log.error(f"Listener '{filename[:-3]}' failed to load: {e}", extra={"locals": locals()})

    def load_routines(self, path: str) -> None:
        for filename in os.listdir(path):
            if not filename.endswith(".py") or filename.startswith("__"):
                continue
            try:
                local: str = os.path.join(path, filename)
                name: str = local[:-3].replace("/", ".")
                package: str = path.replace("/", ".")
                module: types.ModuleType = import_module(name, package=package)
                routine: Routine = Routine(
                    coro=module.routine,
                    time=getattr(module, "time", None),
                    delta=getattr(module, "delta", None),
                )
                self.routines.append(routine)
                log.info(f"Routine '{filename[:-3]}' loaded with time/delta '{routine._time or routine._delta}'")
            except Exception as e:
                log.error(f"Routine '{filename[:-3]}' failed to load: {e}", extra={"locals": locals()})

    def load_cogs(self, base: str = "somali/cogs") -> None:
        self.add_checks()
        for cog in os.listdir(base):
            paths: str = os.listdir(os.path.join(base, cog))
            if "commands" in paths:
                self.load_commands(os.path.join(base, cog, "commands"))
            if "listeners" in paths:
                self.load_listeners(os.path.join(base, cog, "listeners"))
            if "routines" in paths:
                self.load_routines(os.path.join(base, cog, "routines"))

    def add_channel(self, name, id, banwords=[], disabled=[], online=True, prefix="+") -> None:
        if name in self.channels:
            log.warning(f"'{name}' already added")
        else:
            self.channels[name] = {
                "id": id, "banwords": banwords, "disabled": disabled, "online": online, "prefix": prefix
            }

    async def add_all_channels(self) -> None:
        channels = await Channel.all().select_related("user")
        if not channels:
            self.add_channel(self.owner.lower(), 0)
        for channel in channels:
            if channel.user.block:
                continue
            self.add_channel(
                channel.user.name,
                channel.user_id,
                list(channel.banwords.keys()),
                list(channel.disabled.keys()),
                channel.online,
                channel.prefix
            )

    async def fetch_blocked(self) -> None:
        self.blocked = await User.filter(block=True).all().values_list("id", flat=True)

    async def reply(self, ctx: Ctx) -> bool:
        if not ctx.response:
            return False
        try:
            ctx.response = f"{ctx.user or ctx.author.name}, {ctx.response}"
            await ctx.send(ctx.response)
        except Exception as e:
            log.error(e, extra={"ctx": dict(ctx)})
        else:
            log.info(f"#{ctx.channel.name} || @{self.nick}: {ctx.response}")
            await Analytics.sent(self.loop, ctx)
            return True
        return False

    async def handle_commands(self, ctx: Ctx) -> bool:
        # await ctx.send("/color OrangeRed")
        if ctx.response:
            # print("entrou em resposta")
            return False
        if not ctx.prefix:
            # print("entrou em prefixo")
            return False
        if not ctx.is_valid:
            # print("entrou em valido", self._prefix)
            return False
        if not ctx.prediction:
            # print("entrou em prediction")
            log.info(f"#{ctx.channel.name} || @{ctx.author.name}: {ctx.message.content}")
            await Analytics.received(self.loop, ctx)
        if not ctx.user:
            # print("entrou em user")
            ctx.user, _ = await User.get_or_create(
                id=ctx.author.id,
                defaults={
                    "channel": ctx.channel.name,
                    "name": ctx.author.name,
                    "color": ctx.author.colour,
                    "content": ctx.message.content.replace("ACTION", "", 1),
                },
            )
        try:
            # print(ctx.prefix, self._prefix)
            # print("entrou em try")
            await self.invoke(ctx)
        except MissingRequiredArgument:
            ctx.response = ctx.command.usage
        except Exception as e:
            log.error(e, extra={"ctx": dict(ctx)})
        return await self.reply(ctx)

    async def handle_mentions(self, ctx: Ctx) -> bool:
        if ctx.response:
            return False
        if not self.mentions:
            return False
        if not ctx.message.content.startswith((self.nick, f"@{self.nick}")):
            return False
        log.info(f"#{ctx.channel.name} || @{ctx.author.name}: {ctx.message.content}")
        await Analytics.received(self.loop, ctx)
        content: str = ctx.message.content.partition(" ")[2]
        prediction: dict = await AI.predict(content)
        intent: str = prediction["intent"]
        entity: str = prediction["entity"]
        confidence: float = prediction["confidence"]
        if intent and confidence > 0.75:
            ctx.message.content: str = f"{self._prefix}{intent} {entity}".strip()
            ctx.response = AI.small_talk(intent)
            return await self.handle_commands(ctx)
        ctx.response = 'não entendi isso, mas tente ver meus comandos digitando "%help"'
        return await self.reply(ctx)

    async def handle_listeners(self, ctx: Ctx) -> bool:
        for listener in self.listeners:
            if ctx.response:
                break
            if inspect.iscoroutinefunction(listener):
                await listener(ctx)
            else:
                listener(ctx)
        return await self.reply(ctx)

    async def event_ready(self) -> None:
        [routine.start(self) for routine in self.routines]
        log.info(f"{self.nick} | #{len(self.channels)} | {self._prefix}{len(self.commands)}")

    async def event_raw_data(self, data) -> None:
        bot_part_prefix = f":{self.nick}!{self.nick}@{self.nick}.tmi.twitch.tv PART"
        if data.startswith(f"{bot_part_prefix} #"):
            i = len(f"{bot_part_prefix} #")
            channel = data[i:].strip("\r\n")
            self._connection._cache.pop(channel)

    async def event_command_error(self, ctx: Ctx, e: Exception) -> None:
        name = ctx.channel.name
        canal1 = await UserPrefix.get(name=name)
        canal = await Channel.get(user_id=canal1.id)
        prefiquiso = ctx.message.content[0]
        if prefiquiso != canal.prefix:
            return
        if prefiquiso == canal.prefix:
            if isinstance(e, CommandIsDisabled):
                ctx.response = "esse comando está desativado nesse canal"
            elif isinstance(e, ContentHasBanword):
                ctx.response = "sua mensagem contém um termo banido"
            elif isinstance(e, UserIsNotAllowed):
                ctx.response = "apenas inscritos, VIPs e MODs podem enviar links"
            elif isinstance(e, InvalidName):
                ctx.response = "nome de usuário inválido"
            elif isinstance(e, GameIsAlreadyRunning):
                ctx.response = "um jogo já está em andamento nesse canal"
            elif isinstance(e, (BotIsOffline, CommandOnCooldown, CommandNotFound, CheckFailure)):
                log.info(e)
            else:
                ctx.response = "ocorreu um erro inesperado"
                log.error(e, extra={"ctx": dict(ctx)}, exc_info=e)
            await self.reply(ctx)
        else:
            return

    async def event_message(self, message: Message) -> None:
        if message.echo:
            return
        if message.author.id in self.blocked:
            return
        ctx: Ctx = await self.get_context(message, cls=Ctx)
        name = message.channel.name
        canal1 = await UserPrefix.get(name=name)
        canal = await Channel.get(user_id=canal1.id)
        prefiquiso = message.content[0]
        # print(prefiquiso,canal.prefix, canal1.id)
        if self.channels[ctx.channel.name]["online"]:
            ctx.user = await User.update_or_none(ctx)
            await self.handle_listeners(ctx)
            await self.handle_mentions(ctx)
        if prefiquiso != canal.prefix:
            return
        if prefiquiso == canal.prefix:
            
            await self.handle_commands(ctx)
        else:
            return
