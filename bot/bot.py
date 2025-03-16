# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import TYPE_CHECKING
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
from tortoise.exceptions import DoesNotExist
from twitchio.ext.routines import Routine
from twitchio.ext.commands import CommandErrorPayload, Command

from bot.exceptions import (
    GuardFailure, CommandNotFound, CommandOnCooldown, DevRequired, InvalidArgument, OwnerRequired,
)
from bot.ext import Bot, Context, ChatMessage, routine
from bot.ext import Config
from bot.models import Channel as ChannelModel, User as UserModel
from bot.models.User_extras import BotsIgnore
from bot.translations import Response, TranslationManager
from bot.utils import (
    CookieTools, LotteryTools, MarkovProcessor, ToolsTools, UploadThings, StringTools, Check
)
from bot.utils.caches import (Cache, SessionsCaches, aioCache)
from bot.utils.command_handler import CommandHandler
from bot.utils.dynamic_descriptions import DynamicDescriptions


import twitchio
from twitchio import eventsub
from twitchio.ext import commands
from bot.models import Channel as ChannelModel, User as UserModel, TwitchTokens
from tortoise.exceptions import DoesNotExist
from bot.ext import Config
from loguru import logger

if TYPE_CHECKING:
    from bot.api import api, api_start


class Gorenmu(Bot):
    def __init__(self, configs: Config, case_insensitive: bool, log: logger, adapter) -> None:
        super().__init__(
                client_id=configs.ApisConfig.api_client_id,
                client_secret=configs.ApisConfig.api_client_secret,
                prefix=configs.BotConfig.prefix,
                case_insensitive=case_insensitive,
                bot_id=configs.BotConfig.bot_id,
                adapter=adapter
        )
        self.log: Logger = log
        self.config: Config = configs
        self.cache: RedisCache | MemcachedCache | SimpleMemoryCache = Cache.cache_load(self)
        self.boot: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
        self.timezone: datetime.timezone = datetime.timezone(datetime.timedelta(hours=-3))
        self.TranslationManager: TranslationManager = TranslationManager(self.config.mock)
        self.docs_handler: DynamicDescriptions = DynamicDescriptions(self)
        self.CommandHandler: CommandHandler = CommandHandler()
        self.SessionsCaches: SessionsCaches = SessionsCaches(self)
        self.MarkovProcessor: MarkovProcessor | None = None
        self.UploadThings: UploadThings = UploadThings(self)
        self.ToolsTools: ToolsTools = ToolsTools(self)
        self.StringTools: StringTools = StringTools()
        self.LotteryTools: LotteryTools = LotteryTools(self)
        self.CookieTools: CookieTools = CookieTools(self)
        self.lottery_lock: asyncio.Lock = asyncio.Lock()
        self.manual_event_message: list[Callable] = []
        self.bots_ids: list[int] = []
        self.dev_name: str
        self.dev_display_name: str
        self.bot_nick: str
        self.api: api | None = None
        self.api_start: api_start = None
        self.channels: dict[str, ChannelModel] = {}
        self.routines: list[callable] = []

    async def setup_hook(self) -> None:
        tokens = await TwitchTokens.all()
        for token in tokens:
            await token.fetch_related("user")
            user: UserModel = token.user
            subscription = eventsub.ChatMessageSubscription(broadcaster_user_id=str(user.id), user_id=str(self.config.BotConfig.bot_id))
            await self.subscribe_websocket(payload=subscription)
            subscription = eventsub.StreamOnlineSubscription(broadcaster_user_id=str(user.id))
            await self.subscribe_websocket(payload=subscription)

        subscription = eventsub.ChatMessageSubscription(broadcaster_user_id=str(self.config.BotConfig.dev_userid), user_id=str(self.config.BotConfig.bot_id))
        await self.subscribe_websocket(payload=subscription)

        subscription = eventsub.StreamOnlineSubscription(broadcaster_user_id=str(self.config.BotConfig.dev_userid))
        await self.subscribe_websocket(payload=subscription)

        subscription = eventsub.WhisperReceivedSubscription(broadcaster_user_id=str(self.config.BotConfig.bot_id), user_id=str(self.config.BotConfig.bot_id))
        await self.subscribe_websocket(subscription)


    async def add_token(self, token: str, refresh: str) -> twitchio.authentication.ValidateTokenPayload:
        resp: twitchio.authentication.ValidateTokenPayload = await super().add_token(token, refresh)

        user = await UserModel.get(id=resp.user_id)
        token_db = await TwitchTokens.get_or_none(user=user)
        if token and token_db.token != token or token_db.refresh != refresh:
            token_db.token = token
            token_db.refresh = refresh
            await token_db.save()
        if not token_db:
            token_db = await TwitchTokens.create(user=user, token=token, refresh=refresh)

        self.log.info(f"Added token to the database for user: {resp.user_id}")
        return resp

    async def load_tokens(self, path: str | None = None) -> None:
        tokens = await TwitchTokens.all()
        for token in tokens:
            await self.add_token(token=token.token, refresh=token.refresh)

    async def setup_database(self) -> None:
        await Tortoise.init(config=self.config.DatabaseConfig.DB_CONFIG)
        await Tortoise.generate_schemas()
        try:
            user = await UserModel.get(id=926706091)
        except DoesNotExist:
            user = await UserModel.create_or_none(926706091, "MrNotChuw")
        try:
            await ChannelModel.get(user=user)
        except DoesNotExist:
            await ChannelModel.create(user=user)

    async def update_channels(self) -> None:
        for channel in await ChannelModel.filter(removed=False):
            self.channels[(await channel.user).name] = channel

    async def is_online(self, message: ChatMessage) -> bool:
        # await self.update_channel()  # Dont need because the disable command update the local cache too.
        return (message.text.startswith(f"{self.channels[message.broadcaster.name].prefix}start") or
                self.channels[message.broadcaster.name].online)

    def is_enabled(self, ctx: Context, command: str = "") -> bool:
        return (command or ctx.command.name.lower()) not in self.channels[ctx.channel.name].disabled

    @staticmethod
    async def close_db() -> None:
        await Tortoise.close_connections()

    async def setup(self):
        bot_list = await BotsIgnore.filter(active=True).all()
        self.bots_ids = [_id.user_id for _id in bot_list]  # NOQA
        self.MarkovProcessor = MarkovProcessor(self)
        await self.update_channels()
        asyncio.create_task(self.MarkovProcessor.process_message(), name="process_message")
        await CommandHandler.load_cogs(self, "bot/cogs")
        if self.config.ApisConfig.enable_site_endpoints:
            asyncio.create_task(self.api_start(self))

    async def close(self) -> None:
        await self.close_db()
        await self.SessionsCaches.close_all_sessions()
        await super().close()

    async def event_ready(self) -> None:
        self.dev_name = (await self.fetch_users(ids=[self.config.BotConfig.dev_userid]))[0].display_name  # NOQA
        self.dev_display_name = self.config.BotConfig.dev_display_name  # NOQA
        self.config.BotConfig.dev_name = self.dev_name
        self.log.info(
                f"{self.bot_id} | {len(self.channels)} Channels | {len(self._get_prefix)} prefix's, "
                f"{len(self.commands)} commands."
        )
        self.bot_nick = (await self.fetch_users(ids=[self.bot_id]))[0].display_name  # NOQA
        await UserModel.get_or_create(id=self.bot_id, name=self.bot_nick)

    async def event_command_error(self, payload: CommandErrorPayload) -> None:
        command: Command[Any, ...] | None = payload.context.command
        if command and command.has_error and payload.context.error_dispatched:
            return

        ctx: Context = payload.context
        error: Exception = payload.exception
        if not self.channels[ctx.channel.name].online:
            return None
        if ctx.prefix != self.channels[ctx.channel.name].prefix:
            return None
        # TODO: Ativar de novo o develop.
        # if self.config.DevelopmentConfig.development:
        #     return None
        ctx.translations = ctx.bot.TranslationManager.get_translations(ctx.user.language or ctx.bot.config.default_lang)
        translations = ctx.translations.Exceptions.BotMainLoopExceptions
        if isinstance(error, CommandNotFound):
            return None
        if isinstance(error, DevRequired):
            await ctx.simple_response(ctx, translations.dev_required)
            self.log.warning(error)
        if isinstance(error, OwnerRequired):
            await ctx.simple_response(ctx, translations.owner_required)
        if isinstance(error, CommandOnCooldown):
            format_string = ctx.translations.SupportTools.TimeTools.Humanize.naturaltime(error.remaining, future=True)
            cooldown_str = translations.command_on_cooldown.format(format_string)
            return await ctx.simple_response(ctx, cooldown_str)
        if isinstance(error, NotImplementedError):
            return await ctx.simple_response(ctx, translations.not_implemented)
        if isinstance(error, InvalidArgument) and ctx.command:
            decorator = ctx.command.decorators[ctx.user.language or ctx.bot.config.default_lang]
            await ctx.reply(decorator.usage)
            return
        if isinstance(error, GuardFailure):
            return None
        self.log.error(error, extra={"ctx": dict(ctx)}, exc_info=error)
        return await ctx.simple_response(ctx, translations.error_not_registered.format(self.dev_name))

    async def user_create_or_update(self, ctx: Context):
        user = await self.cache.get(key=int(ctx.author.id), namespace="user")
        if not user:
            user = await UserModel.create_or_update(ctx)
            await self.cache.set(key=int(ctx.author.id), value=user, namespace='user')
        else:
            await UserModel.update_user(user, ctx)

        if not user.translations or user.translations.lang != user.language:
            channel = ctx.channel.name
            channel = ctx.bot.channels[channel]
            translations = ctx.bot.TranslationManager.get_translations(user.language or channel.language or "en")
            user.translations = translations

        return user

    async def event_message(self, payload: ChatMessage):
        if payload.chatter.id == str(self.bot_id) or payload.source_broadcaster is not None:
            return
        ctx: Context = await self.get_context(payload)
        ctx.user, is_online = await asyncio.gather(
                self.user_create_or_update(ctx),
                self.is_online(payload)
        )
        if not is_online:
            return

        ctx.message.text = ctx.message.text.replace("\U000e0000", "")
        if ctx.prefix in ctx.message.text:
            ctx._get_command()  # NOQA
        if not ctx.command:
            await self.MarkovProcessor.put_markov_queue(ctx)

        try:
            channel = self.channels[payload.broadcaster.name]
            if not channel.online and "start" not in payload.text:
                return None
            response: Response | None = None
            if ctx.command:
                self.log.info(f"#{ctx.channel.name}|| @{ctx.author.name}: {ctx.message.text}")

                has_double_prefix = f"{ctx.prefix}{ctx.prefix}" in ctx.message.text
                message_has_pipe = " | " in ctx.message.text
                is_alias_command = f"{ctx.prefix}alias" in ctx.message.text
                if has_double_prefix:
                    response = await ctx.alias_handler(ctx, payload)
                elif message_has_pipe and not is_alias_command:
                    await ctx.pipe_handler(ctx, payload)
                else:
                    response = await self.invoke(ctx)
                if response:
                    await ctx.response(response)
            await self.listeners(ctx)

        except InvalidArgument:
            if ctx.command and hasattr(ctx.command, "usage"):
                decorator = ctx.command.decorators[ctx.user.language]
                return await ctx.reply(decorator.usage)

            error_not_registered = ctx.user.translations.Exceptions.BotMainLoopExceptions.error_not_registered
            return await ctx.simple_response(ctx, error_not_registered.format(self.config.BotConfig.dev_name))
        except Exception as error:
            self.log.error(error, extra={"ctx": dict(ctx)}, exc_info=error)

    @commands.Component.listener('Whisper')
    async def event_message_whisper(self, payload: twitchio.Whisper):
        ctx: Context = await self.get_context(payload)
        ...


    async def listeners(self, ctx):
        if not ctx.user:
            ctx.user = await self.user_create_or_update(ctx)
        for listener in self.manual_event_message:
            if response := await listener(ctx):
                await ctx.response(response)


    async def global_guard(self, ctx: commands.Context) -> bool:
        checks = [Check.online, Check.enabled, Check.banword]
        for check in checks:
            if not check(ctx):
                return False
        return True


















