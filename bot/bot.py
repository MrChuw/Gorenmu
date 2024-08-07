# -*- coding: utf-8 -*-
import asyncio
import contextlib
import datetime
import os
import sys
from logging import Logger
from typing import Any, Callable, Coroutine

from aiocache.backends.memcached import MemcachedCache
from aiocache.backends.memory import SimpleMemoryCache
from aiocache.backends.redis import RedisCache
from loguru import logger
from tortoise import Tortoise
from twitchio.ext.routines import Routine

from bot.exceptions import (
    CheckFailure, CommandNotFound, CommandOnCooldown, DevRequired, InvalidArgument, OwnerRequired,
)
from bot.ext.commands import Bot, Context, Message, routine
from bot.ext.config import Config
from bot.models import Channel as ChannelModel, User as UserModel
from bot.models.User_extras import BotsIgnore
from bot.translations import TranslationManager, Response
from bot.utils import (
    BooruTools, CookieTools, LotteryTools, MarkovProcessor, ToolsTools, UploadThings,
)
from bot.utils.caches import (Cache, SessionsCaches)
from bot.utils.command_handler import CommandHandler


class Gorenmu(Bot):
    event_message_listeners: list[Callable[[Context], Coroutine[Any, Any, bool | Response]]] = []
    routines: list[Routine] = []
    channels: dict[str, ChannelModel] = {}

    def __init__(self, configs: Config, case_insensitive: bool, retain_cache: bool, log: logger) -> None:
        super().__init__(token=configs.ApisConfig.access_token, client_id=configs.ApisConfig.client_id,
                         client_secret=configs.ApisConfig.api_client_secret, prefix=configs.BotConfig.prefix,
                         case_insensitive=case_insensitive, retain_cache=retain_cache, )
        self.log: Logger = log
        self.config: Config = configs
        self.cache: RedisCache | MemcachedCache | SimpleMemoryCache = Cache.cache_load(self)
        self.boot: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
        self.timezone: datetime.timezone = datetime.timezone(datetime.timedelta(hours=-3))
        self.config: Config
        self.CommandHandler: CommandHandler = CommandHandler()
        self.SessionsCaches: SessionsCaches = SessionsCaches(self)
        self.MarkovProcessor: MarkovProcessor | None = None
        self.UploadThings: UploadThings = UploadThings(self)
        self.ToolsTools: ToolsTools = ToolsTools(self)
        self.LotteryTools: LotteryTools = LotteryTools(self)
        self.CookieTools: CookieTools = CookieTools(self)
        self.BooruTools: BooruTools = BooruTools(self.SessionsCaches.BooruCachedSession.cache)
        self.aposta_lock: asyncio.Lock = asyncio.Lock()
        self.TranslationManager: TranslationManager = TranslationManager()
        self.reconnection_attempts: dict[str, int] = {}
        self.bots_ids: list[int] = []
        self.dev_name: str = ""
        self.restart = 0

    async def fetch_channels(self) -> None:
        for channel in await ChannelModel.filter(removed=False):
            self.channels[(await channel.user).name]: ChannelModel = channel

    async def is_online(self, message: Message) -> bool:
        await self.fetch_channels()
        return (self.channels[message.channel.name].online or message.content.startswith(
                f"{self.channels[message.channel.name].prefix}start"
        ))

    def is_enabled(self, ctx: Context, command: str = "") -> bool:
        if "WHISPER" in ctx.message.raw_data:
            return True
        return (command or ctx.command.name.lower()) not in self.channels[ctx.channel.name].disabled

    async def before_connect(self) -> None:
        self.check(self.is_enabled)

    async def after_connect(self) -> None:
        self.check_channels.start()
        self.heart_beat.start()

    @routine(seconds=10, wait_first=True)
    async def check_channels(self) -> None:
        connected_channels = [channel.name for channel in self.connected_channels]
        disconnected_channels = [channel for channel in self.channels.keys() if channel not in connected_channels]
        if disconnected_channels:
            self.log.warning(
                    f"channels={len(connected_channels)}/{len(self.channels)} disconnected_channels={disconnected_channels}"
            )
            try:
                users = await self.fetch_users(disconnected_channels)
                for user in users:
                    user_db = await UserModel.get(id=user.id)
                    if user_db.name != user.name:
                        user_db.name = user.name
                        await user_db.save()
                        users[users.index(user_db.name)] = user_db.name

                await self.join_channels(disconnected_channels)
            except Exception as e:
                self.log.error(e)

            await asyncio.sleep(1)
            disconnected_channels = [channel for channel in self.channels.keys() if channel not in connected_channels]
            for channel in disconnected_channels:
                await asyncio.sleep(0.5)
                try:
                    await self._connection.send(f"JOIN #{channel}\r\n")
                    self.reconnection_attempts[channel] = 0
                except Exception as e:
                    self.log.error(e)
                if channel in self.reconnection_attempts:
                    self.reconnection_attempts[channel] += 1
                else:
                    self.reconnection_attempts[channel] = 1

                if self.reconnection_attempts[channel] >= 10:
                    self.log.warning(f"Failed to connect to #{channel} after {self.max_attempts} attempts. "
                                     f"Removing from database."
                                     )
                    self.channels[channel].removed = True
                    await self.channels[channel].save()
                    self.part_channels([channel])
                    del self.channels[channel]
                else:
                    self.log.info(f"Reconnection attempt {self.reconnection_attempts[channel]} for #{channel}")

        keys_to_remove = [channel for channel in self.reconnection_attempts if channel in connected_channels]
        for key in keys_to_remove:
            del self.reconnection_attempts[key]

    @routine(seconds=60, wait_first=True)
    async def heart_beat(self):
        if self.config.DevelopmentConfig.development:
            return None
        try:
            now = datetime.datetime.now(datetime.UTC)
            seconds_util_next_minute = 60 - now.second
            await asyncio.sleep(seconds_util_next_minute)
            message = f"{self.boot.strftime('%d/%m/%Y %H:%M:%S')} BOT ONLINE"
            name = self.nick
            await self.get_channel(name).send(message)
        except Exception as e:
            logger.error(e)
            os.execv(sys.executable, ["python3.10"] + sys.argv)

    async def connect_db(self) -> None:
        await Tortoise.init(config=self.config.DatabaseConfig.DB_CONFIG)
        await Tortoise.generate_schemas()

    async def before_close(self) -> None:
        self.check_channels.stop()

    async def after_close(self) -> None:
        ...

    def start(self) -> None:
        self.loop.run_until_complete(self.connect_db())
        bot_list = self.loop.run_until_complete(BotsIgnore.filter(active=True).all())
        self.bots_ids = [_id.user_id for _id in bot_list]
        self.MarkovProcessor = MarkovProcessor(self)
        self.loop.run_until_complete(self.before_connect())
        self.loop.run_until_complete(self.fetch_channels())
        self.loop.create_task(self.connect(), name="IRC connect")
        self.loop.create_task(self.MarkovProcessor.process_message(), name="process_message")
        self.loop.run_until_complete(self.after_connect())

    def stop(self) -> None:
        ...

    async def event_ready(self) -> None:  # Load de comando está desativado.
        self.restart += 1
        if self.restart > 1:
            os.execv(sys.executable, ["python3.10"] + sys.argv)
        CommandHandler.load_cogs(self)
        self.dev_name = (await self.fetch_users(ids=[self.config.BotConfig.dev_userid]))[0].display_name
        await self.join_channels([self.dev_name])
        await asyncio.sleep(1)
        self.log.info(
                f"{self.nick} | #({len(self.connected_channels)}/{len(self.channels)}) | {len(self._prefix)} prefix's, "
                f"{len(self.commands)} commands."
        )

    async def global_before_invoke(self, ctx: Context) -> None:  # NOQA
        if ctx.message.content:
            ctx.message.content.replace("\U000e0000", "")
        if "user" not in ctx.__dict__:
            ctx.user = await UserModel.create_or_update(ctx)

    async def event_command_error(self, ctx: Context, error: Exception) -> None:
        if not self.channels[ctx.channel.name].online:
            return None
        if ctx.prefix != self.channels[ctx.channel.name].prefix:
            return None
        # TODO: Ativar de novo o develop.
        # if self.config.DevelopmentConfig.development:
        #     return None
        ctx.translations = ctx.bot.TranslationManager.get_translations(ctx.user.language or "pt-br")
        ctx.decorators = ctx.bot.TranslationManager.get_decorator(ctx.user.language or "pt-br")
        translations = ctx.translations.Exceptions.BotMainLoopExceptions()
        if isinstance(error, CommandNotFound):
            return None
        if isinstance(error, DevRequired):
            await ctx.simple_response(ctx, translations.dev_required)
            self.log.warning(error)
        if isinstance(error, OwnerRequired):
            await ctx.simple_response(ctx, translations.owner_required)
        if isinstance(error, CheckFailure):
            return None
        if isinstance(error, CommandOnCooldown):
            cooldown_str = translations.command_on_cooldown.format(
                    ctx.translations.SupportTools.Humanize.Humanize.naturaltime(error.retry_after, future=True)
            )
            return await ctx.simple_response(ctx, cooldown_str)
        if isinstance(error, NotImplementedError):
            return await ctx.simple_response(ctx, translations.not_implemented)
        if isinstance(error, InvalidArgument) and ctx.command and hasattr(ctx.command, "usage"):
            return await ctx.reply(ctx.decorators.get_usage(ctx, ctx))
        self.log.error(error, extra={"ctx": dict(ctx)}, exc_info=error)
        return await ctx.simple_response(ctx, translations.error_not_registered.format(self.dev_name))

    async def event_message(self, message: Message) -> None:
        if message.echo or message.author.name == self.nick:
            return None
        with contextlib.suppress(IndexError, CommandNotFound):
            ctx: Context | None = await self.get_context(message, cls=Context)
        if ctx and "WHISPER" not in ctx.message.raw_data:
            await self.cache.set(f"{ctx.author.id}", Cache.UserCache(ctx), namespace="UserCache")
            ctx.user = await UserModel.create_or_update(ctx)
            if not ctx.command:
                await self.MarkovProcessor.put_markov_queue(ctx)

            if not await self.is_online(message):
                return None
            try:
                channel = self.channels[message.channel.name]
                prefix = message.content[0] if len(channel.prefix) != 2 else message.content[:2]

                if (
                        channel.online is False and "start" not in message.content or
                        prefix == "ƚ" and channel.online is False):
                    return None
                response: Response | None = None
                if prefix == channel.prefix:
                    ctx.prefix = prefix
                    self.log.info(f"#{ctx.channel.name}|| @{ctx.author.name}: {ctx.message.content}")
                    if " | " not in ctx.message.content:
                        response = await self.invoke(ctx)
                    if response:
                        await ctx.response(response)
                    if " | " in ctx.message.content:
                        await ctx.pipe_handler(message, ctx)

            except InvalidArgument:
                if ctx.command and hasattr(ctx.command, "usage"):
                    return await ctx.reply(ctx.decorators.get_usage(ctx, ctx))
                return await ctx.simple_response(ctx,
                                                 ctx.translations.Exceptions.BotMainLoopExceptions.
                                                 error_not_registered.format(self.fetch_users(
                                                 [self.config.BotConfig.dev_userid])[0]))
            except Exception as error:
                self.log.error(error, extra={"ctx": dict(ctx)}, exc_info=error)
            else:
                # TODO: Talvez mudar os checks dos listernes para ca ou tentar criar o
                #  próprio sistema de check igual comandos.
                if not ctx.user:
                    ctx.user = await UserModel.create_or_update(ctx)
                for listener in self.event_message_listeners:
                    if response := await listener(ctx):
                        await ctx.response(response)

        if ctx and "WHISPER" in ctx.message.raw_data:  # TODO: Fazer o handler de whisper.
            # await self.invoke(ctx)
            #
            #   Criar uma implementacao para lidar com os whispers, utilizando cooldown e custom parser para o get_context.
            #   Caso a versão 3 do twitchio não ja tenha resolvido.
            #
            ...
