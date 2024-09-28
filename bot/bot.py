# -*- coding: utf-8 -*-
import asyncio
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
from bot.ext import Bot, Context, Message, routine
from bot.ext import Config
from bot.models import Channel as ChannelModel, User as UserModel
from bot.models.User_extras import BotsIgnore
from bot.translations import Response, TranslationManager
from bot.utils import (
    CookieTools, LotteryTools, MarkovProcessor, ToolsTools, UploadThings, StringTools
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
                         case_insensitive=case_insensitive, retain_cache=retain_cache)
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
        self.StringTools: StringTools = StringTools()
        self.LotteryTools: LotteryTools = LotteryTools(self)
        self.CookieTools: CookieTools = CookieTools(self)
        self.lottery_lock: asyncio.Lock = asyncio.Lock()
        self.TranslationManager: TranslationManager = TranslationManager(self.config.mock)
        self.reconnection_attempts: dict[str, int] = {}
        self.bots_ids: list[int] = []
        self.dev_name: str = ""
        self.restart = 0
        self.alias_cache: SimpleMemoryCache = Cache.create_cache()

    async def fetch_channels(self) -> None:
        for channel in await ChannelModel.filter(removed=False):
            self.channels[(await channel.user).name]: ChannelModel = channel

    async def is_online(self, message: Message) -> bool:
        await self.fetch_channels()

        return (message.content.startswith(f"{self.channels[message.channel.name].prefix}start") or self.channels[
            message.channel.name].online)

    def is_enabled(self, ctx: Context, command: str = "") -> bool:
        if ".tmi.twitch.tv WHISPER" in ctx.message.raw_data:
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
            self.log.warning(f"channels={len(connected_channels)}/{len(self.channels)} "
                             f"disconnected_channels={disconnected_channels}"
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
                await asyncio.sleep(1)
            except Exception as e:
                self.log.error(e)

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

                if self.reconnection_attempts[channel] == 9:
                    self.log.warning(f"last attempt to try to connect to the #{channel} channel.")
                    user = await self.fetch_users(names=[channel])
                    await self.join_channels(channels=[user.name])

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
            if venv_python := os.getenv("VIRTUAL_ENV"):
                python_executable = os.path.join(venv_python, "bin", "python")
            else:
                python_executable = sys.executable
            os.execv(python_executable, [python_executable] + sys.argv)

    async def connect_db(self) -> None:
        await Tortoise.init(config=self.config.DatabaseConfig.DB_CONFIG)
        await Tortoise.generate_schemas()

    @staticmethod
    async def close_db() -> None:
        await Tortoise.close_connections()

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
        CommandHandler.load_cogs(self, "bot/cogs")

    def stop(self) -> None:
        self.loop.run_until_complete(self.close_db())
        self.loop.run_until_complete(self.before_close())
        self.loop.run_until_complete(self.SessionsCaches.close_all_sessions())

    async def event_ready(self) -> None:  # Load de comando está desativado.
        self.restart += 1
        if self.restart > 1:
            if venv_python := os.getenv("VIRTUAL_ENV"):
                python_executable = os.path.join(venv_python, "bin", "python")
            else:
                python_executable = sys.executable
            os.execv(python_executable, [python_executable] + sys.argv)
        self.dev_name = (await self.fetch_users(ids=[self.config.BotConfig.dev_userid]))[0].display_name
        await self.join_channels([self.dev_name])
        await asyncio.sleep(1)
        self.log.info(
                f"{self.nick} | #({len(self.connected_channels)}/{len(self.channels)}) | {len(self._prefix)} prefix's, "
                f"{len(self.commands)} commands."
        )

        await UserModel.get_or_create(id=self.user_id, name=self.nick)

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
        ctx.translations = ctx.bot.TranslationManager.get_translations(ctx.user.language or "en")
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
                    ctx.translations.SupportTools.Humanize.naturaltime(error.retry_after, future=True)
            )
            return await ctx.simple_response(ctx, cooldown_str)
        if isinstance(error, NotImplementedError):
            return await ctx.simple_response(ctx, translations.not_implemented)
        if isinstance(error, InvalidArgument) and ctx.command:
            decorator = ctx.command.decorators[ctx.user.language]
            return await ctx.reply(decorator.get_usage(ctx))
        self.log.error(error, extra={"ctx": dict(ctx)}, exc_info=error)
        return await ctx.simple_response(ctx, translations.error_not_registered.format(self.dev_name))

    async def listeners(self, ctx):
        if not ctx.user:
            ctx.user = await UserModel.create_or_update(ctx)
        for listener in self.event_message_listeners:
            if response := await listener(ctx):
                await ctx.response(response)

    async def event_message(self, message: Message) -> None:
        if message.echo or message.author.name == self.nick:
            return None
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
                self.CommandHandler.load_language(ctx)
                await self.listeners(ctx)
                if (channel.online is False and "start" not in message.content or ctx.prefix == "ƚ"
                        and channel.online is False):
                    return None
                response: Response | None = None
                if ctx.command:
                    self.log.info(f"#{ctx.channel.name}|| @{ctx.author.name}: {ctx.message.content}")

                if f"{ctx.prefix}{ctx.prefix}" in ctx.message.content:
                    response = await ctx.alias_handler(ctx, message)
                elif " | " not in ctx.message.content or f"{ctx.prefix}alias" in ctx.message.content:
                    response = await self.invoke(ctx)
                elif " | " in ctx.message.content and f"{ctx.prefix}alias" not in ctx.message.content:
                    await ctx.pipe_handler(ctx, message)
                if response:
                    await ctx.response(response)

            except InvalidArgument:
                if ctx.command and hasattr(ctx.command, "usage"):
                    decorator = ctx.command.decorators[ctx.user.language]
                    return await ctx.reply(decorator.get_usage(ctx))
                return await ctx.simple_response(ctx,
                                                 ctx.translations.Exceptions.BotMainLoopExceptions.error_not_registered
                                                 .format(self.fetch_users([self.config.BotConfig.dev_userid])[0]))
            except Exception as error:
                self.log.error(error, extra={"ctx": dict(ctx)}, exc_info=error)


        if ctx and ".tmi.twitch.tv WHISPER" in ctx.message.raw_data:
            ctx.author.id = ctx.message.tags["user-id"]
            ctx.user = await UserModel.get(id=ctx.author.id)
            try:
                # response: Response | None = None
                ctx.prefix = "+"
                self.log.info(f"whispers || @{ctx.author.name}: {ctx.message.content}")
                if " | " not in ctx.message.content:
                    await self.invoke(ctx)
                    # TODO: Need a method of responding to whispers

            except InvalidArgument:
                if ctx.command and hasattr(ctx.command, "usage"):
                    decorator = ctx.command.decorators[ctx.user.language]
                    return await ctx.reply(decorator.get_usage(ctx, ctx))
                return await ctx.simple_response(ctx,
                                                 ctx.translations.Exceptions.BotMainLoopExceptions.error_not_registered
                                                 .format(self.fetch_users([self.config.BotConfig.dev_userid])[0]))
            except Exception as error:
                self.log.error(error, extra={"ctx": dict(ctx)}, exc_info=error)

    async def event_error(self, error: Exception, data: str = None) -> None:
        if data is not None:
            self.log.error(str(data.args), exc_info=error)
        if "'Context' object has no attribute 'user'" not in error.args:
            self.log.error(str(error.args), exc_info=data)
































