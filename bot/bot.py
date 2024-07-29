

# -*- coding: utf-8 -*-
import asyncio
import contextlib
import datetime
import os
import sys
from logging import Logger
from typing import Any, Callable, Coroutine

import humanize
import pytz
from aiocache.backends.memcached import MemcachedCache
from aiocache.backends.memory import SimpleMemoryCache
from aiocache.backends.redis import RedisCache
from pytz import reference as pytz_reference
from tortoise import Tortoise
from twitchio.ext.routines import Routine


from bot.ext.commands import Bot, Context, Message, routine

from bot.models import Bots_ignore, Channel as ChannelModel, Loterica, User as UserModel
from translations import TranslationManager
from .exceptions import (CheckFailure, CommandNotFound, CommandOnCooldown, DevRequired, InvalidArgument, OwnerRequired)
from bot.utils import (
    BooruTools, Check, CommandHandler, Convert, CookieTools, Dicio, LotteryTools, MarkovProcessor, Rand, Role,
    Selenium, TimeTools, ToolsTools, UploadThings,
)


import asyncio
import datetime
from logging import Logger
from typing import Any, Callable, Coroutine
from bot.utils.caches import (Cache, SessionsCaches)


import humanize
from twitchio.ext.routines import Routine
from bot.ext.config import Config
from bot.ext.commands import Bot, Context
from bot.translations import TranslationManager
from bot.utils.command_handler import  CommandHandler

from bot.models import Channel as ChannelModel



class Gorenmu(Bot):
    event_message_listeners: list[Callable[[Context], Coroutine[Any, Any, bool]]] = []
    routines: list[Routine] = []
    channels: dict[str, ChannelModel] = {}

    def __init__(self, configs: Config, case_insensitive: bool, retain_cache: bool, log: Logger) -> None:
        super().__init__(
                token=configs.ApisConfig.access_token,
                client_id=configs.ApisConfig.client_id,
                client_secret=configs.ApisConfig.api_client_secret,
                prefix=configs.BotConfig.prefix,
                case_insensitive=case_insensitive,
                retain_cache=retain_cache,
        )
        self.log: Logger = log
        self.config: Config = configs
        self.cache: RedisCache | MemcachedCache | SimpleMemoryCache = Cache.cache_load(self)
        self.boot: datetime.datetime = datetime.datetime.utcnow()
        self.timezone: datetime.timezone = datetime.timezone(datetime.timedelta(hours=-3))
        self.config: Config
        self.CommandHandler: CommandHandler = CommandHandler()
        self.SessionsCaches: SessionsCaches = SessionsCaches(self)
        self.MarkovProcessor: MarkovProcessor
        self.UploadThings: UploadThings = UploadThings(self)
        self.ToolsTools: ToolsTools = ToolsTools(self)

        self.LotteryTools: LotteryTools = LotteryTools(self)
        self.CookieTools: CookieTools = CookieTools(self)
        self.BooruTools: BooruTools = BooruTools(self.SessionsCaches.BooruCachedSession.cache)
        self.Dicio: Dicio = Dicio()
        self.humanize: humanize = humanize
        self.aposta_lock: asyncio.Lock = asyncio.Lock()
        self.TranslationManager: TranslationManager = TranslationManager()






















































