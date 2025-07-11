# -*- coding: utf-8 -*-
from __future__ import annotations

import asyncio
import datetime
from asyncio import Task
from collections import defaultdict
from logging import Logger
from typing import Callable, TYPE_CHECKING

import twitchio
from aiocache.backends.memcached import MemcachedCache
from aiocache.backends.memory import SimpleMemoryCache
from aiocache.backends.redis import RedisCache
from loguru import logger
from twitchio.ext import commands
from twitchio.ext.commands import CommandErrorPayload

from bot.apis import Emotes
from bot.ext import ChatMessage
from bot.handlers import (
    ChannelHandler, CommandHandler, ContextHandler, DatabaseHandler, LifecycleHandler, TokensHandler,
)
from bot.translations import TranslationManager
from bot.utils import (
    Cache, Config, DynamicDescriptions, MarkovProcessor, MemCache, SessionsCaches, StringTools, TimeTools, UploadThings,
)

if TYPE_CHECKING:
    # from bot.api import api, api_start
    from bot.models import Channel as ChannelModel
    from bot.ext import Routine, Context


class Gorenmu(commands.AutoBot):
    def __init__(self, configs: Config, case_insensitive: bool, log: logger, adapter) -> None:
        super().__init__(
            client_id=configs.ApisConfig.api_client_id,
            client_secret=configs.ApisConfig.api_client_secret,
            prefix=configs.BotConfig.prefix,
            case_insensitive=case_insensitive,
            bot_id=configs.BotConfig.bot_id,
            adapter=adapter,
        )
        self.boot: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
        self.lottery_lock: asyncio.Lock = asyncio.Lock()
        self.channels: dict[str, ChannelModel] = {}
        self.routines: list[Routine] = []
        self.bots_ids: list[int] = []
        self.manual_event_message: list[Callable] = []
        # self.api: api | None = None
        # self.api_start: api_start = None
        self.MarkovProcessor: MarkovProcessor | None = None
        self.MarkovTask: Task[None] | None = None
        self.dev_name: str | None = None
        self.dev_display_name: str
        self.bot_nick: str | None = None
        self.log: Logger = log
        self.config: Config = configs
        self.memcache: MemCache = MemCache()
        self.StringTools: StringTools = StringTools()
        self.cache: RedisCache | MemcachedCache | SimpleMemoryCache = Cache.cache_load(bot=self)
        self.docs_handler: DynamicDescriptions = DynamicDescriptions(self)
        self.UploadThings: UploadThings = UploadThings(self)
        self.docs: defaultdict = defaultdict(dict)

        self.SessionsCaches: SessionsCaches = SessionsCaches(self)
        self.TranslationManager: TranslationManager = TranslationManager()
        self.Emotes: Emotes = Emotes(bot=self)
        self.TokensHandler: TokensHandler = TokensHandler(bot=self)
        self.DatabaseHandler: DatabaseHandler = DatabaseHandler(bot=self)
        self.ChannelHandler: ChannelHandler = ChannelHandler(bot=self)
        self.CommandHandler: CommandHandler = CommandHandler(bot=self)
        self.LifecycleHandler: LifecycleHandler = LifecycleHandler(bot=self)
        self.ContextHandler: ContextHandler = ContextHandler(bot=self)
        self.TimeTools: TimeTools = TimeTools()
        self.mock: bool = False

    async def add_token(self, token: str, refresh: str) -> twitchio.authentication.ValidateTokenPayload:
        return await self.TokensHandler.add_token(token, refresh)

    async def load_tokens(self, path: str | None = None) -> None:
        await self.TokensHandler.load_tokens(path)

    async def event_oauth_authorized(self, payload: twitchio.authentication.UserTokenPayload) -> None:
        await self.TokensHandler.event_oauth_authorized(payload)

    async def reload_component(self, attr_name: str, module_name: str, class_name: str, args: list = None):
        from bot.utils.reload_util import reload_and_get

        try:
            new_class = reload_and_get(module_name, class_name)
            instance = new_class(*args) if args else new_class()
            old_instance = getattr(self, attr_name)
            if getattr(old_instance, "close", None):
                old_instance.close()
            setattr(self, attr_name, instance)
            self.log.info(f"Reloaded {attr_name} from {module_name}.{class_name}")
        except Exception as e:
            self.log.error(f"Error reloading {attr_name}: {e}")
            raise

    async def close(self) -> None:
        await self.LifecycleHandler.close()

    async def event_ready(self) -> None:
        await self.LifecycleHandler.event_ready()

    async def event_command_error(self, payload: CommandErrorPayload) -> None:
        return await self.CommandHandler.event_command_error(payload)

    async def event_message(self, payload: ChatMessage):
        return await self.LifecycleHandler.event_message(payload)

    @commands.Component.listener("Whisper")
    async def event_message_whisper(self, payload: twitchio.Whisper):
        return await self.event_message_whisper(payload)

    async def global_guard(self, ctx: Context) -> bool:
        return await self.LifecycleHandler.global_guard(ctx)

    async def get_context(self: Gorenmu, payload: ChatMessage | twitchio.Whisper, *, cls: Context = None) -> Context:
        return await self.LifecycleHandler.get_context(payload)
