from __future__ import annotations

import datetime
from collections import defaultdict
from collections.abc import Callable
from logging import Logger
from typing import TYPE_CHECKING

import twitchio
from aiocache.backends.memcached import MemcachedCache
from aiocache.backends.memory import SimpleMemoryCache
from aiocache.backends.redis import RedisCache
from twitchio.ext import commands
from twitchio.ext.commands import CommandErrorPayload

from bot.ext import ChatMessage, TypesBot
from bot.handlers import (
    ChannelHandler,
    CommandHandler,
    ContextHandler,
    DatabaseHandler,
    LifecycleHandler,
    TokensHandler,
)
from bot.utils import Cache, Config, MemCache, TimeTools

if TYPE_CHECKING:
    # from bot.api import api, api_start
    from bot.ext import Context


class Gorenmu(TypesBot):
    def __init__(self, configs: Config, case_insensitive: bool, log: Logger, adapter) -> None:
        super().__init__(
            client_id=configs.ApisConfig.api_client_id,
            client_secret=configs.ApisConfig.api_client_secret,
            prefix=configs.BotConfig.prefix,
            case_insensitive=case_insensitive,
            bot_id=configs.BotConfig.bot_id,
            adapter=adapter,
        )
        self.boot: datetime.datetime = datetime.datetime.now(datetime.UTC)
        self.manual_events: defaultdict[str, dict[str, dict[str, Callable]]] = defaultdict(lambda: defaultdict(dict))
        # self.api: api | None = None
        # self.api_start: api_start = None
        self.log: Logger = log
        self.config: Config = configs
        self.memcache: MemCache = MemCache()
        self.cache: RedisCache | MemcachedCache | SimpleMemoryCache = Cache.cache_load(bot=self)
        self.TokensHandler: TokensHandler = TokensHandler(bot=self)
        self.DatabaseHandler: DatabaseHandler = DatabaseHandler(bot=self)
        self.ChannelHandler: ChannelHandler = ChannelHandler(bot=self)
        self.CommandHandler: CommandHandler = CommandHandler(bot=self)
        self.LifecycleHandler: LifecycleHandler = LifecycleHandler(bot=self)
        self.ContextHandler: ContextHandler = ContextHandler(bot=self)
        self.TimeTools: TimeTools = TimeTools()

    async def add_token(self, token: str, refresh: str) -> twitchio.authentication.ValidateTokenPayload:
        return await self.TokensHandler.add_token(token, refresh)

    async def load_tokens(self, path: str | None = None) -> None:
        await self.TokensHandler.load_tokens(path)

    async def event_oauth_authorized(self, payload: twitchio.authentication.UserTokenPayload) -> None:
        await self.TokensHandler.event_oauth_authorized(payload)

    async def close(self) -> None:
        await self.LifecycleHandler.close()

    async def event_ready(self) -> None:
        await self.LifecycleHandler.event_ready()

    @commands.Component.listener("Whisper")
    async def event_message_whisper(self, payload: twitchio.Whisper):
        return await self.event_message_whisper(payload)

    async def global_guard(self, ctx: Context) -> bool:
        return await self.LifecycleHandler.global_guard(ctx)

    async def get_context(self: Gorenmu, payload: ChatMessage | twitchio.Whisper, *, cls: Context = None) -> Context:
        return await self.LifecycleHandler.get_context(payload)

    async def before_invoke(self, ctx: Context) -> None:
        await self.LifecycleHandler.before_invoke(ctx)

    async def after_invoke(self, ctx: Context) -> None:
        await self.LifecycleHandler.after_invoke(ctx)

    async def event_command_invoked(self, ctx: Context) -> None:
        await self.LifecycleHandler.event_command_invoked(ctx)

    async def event_command_completed(self, ctx: Context) -> None:
        await self.LifecycleHandler.event_command_completed(ctx)

    async def event_command_error(self, payload: CommandErrorPayload) -> None:
        return await self.CommandHandler.event_command_error(payload)

    async def event_message(self, payload: ChatMessage):
        return await self.LifecycleHandler.event_message(payload)
