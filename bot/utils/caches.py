# -*- coding: utf-8 -*-
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, TYPE_CHECKING

import redis
from aiocache import Cache as aioCache
from aiocache.backends.memcached import MemcachedCache
from aiocache.backends.memory import SimpleMemoryCache
from aiocache.backends.redis import RedisCache
from aiocache.serializers import PickleSerializer
from aiohttp_client_cache import CachedSession, RedisBackend, SQLiteBackend, CacheBackend

from bot.ext.config import CacheType
import aiohttp

from collections import OrderedDict
from threading import RLock
from time import time
from typing import Any, Optional
from aiohttp_client_cache import CachedResponse, CachedSession
import asyncio

if TYPE_CHECKING:
    from bot.bot import Gorenmu

CODE_LIST = (200, 201, 202, 204, 301, 302, 304, 400, 401, 403, 404, 405, 408, 409, 410, 500, 501, 502, 503, 504)

__all__ = ("SessionsCaches", "Cache", "aioCache")


class Cache:
    @staticmethod
    def cache_load(bot: Gorenmu) -> RedisCache | MemcachedCache | SimpleMemoryCache:
        if bot.config.CacheConfig.type in [CacheType.REDIS, CacheType.VALKEY]:
            bot.cache = aioCache(aioCache.REDIS, serializer=PickleSerializer(), endpoint=bot.config.CacheConfig.host,
                                 port=bot.config.CacheConfig.port, namespace=bot.config.CacheConfig.namespace, )
            bot.redis = redis.Redis(host=bot.cache.endpoint, port=bot.cache.port, decode_responses=True)
        elif bot.config.CacheConfig.type == CacheType.MEMCACHED:
            bot.cache = aioCache(aioCache.MEMCACHED, serializer=PickleSerializer(), endpoint="localhost", port=11211,
                                 namespace=bot.config.CacheConfig.namespace
                                 )
        elif bot.config.CacheConfig.type == CacheType.MEMORY:
            bot.cache = aioCache(aioCache.MEMORY, namespace=bot.config.CacheConfig.namespace)
        else:
            bot.cache = aioCache(aioCache.MEMORY, namespace=bot.config.CacheConfig.namespace)
        return bot.cache

    @staticmethod
    def create_cache(namespace: str = "main") -> RedisCache | MemcachedCache | SimpleMemoryCache:
        return aioCache(aioCache.MEMORY, namespace=namespace)


class BaseCachedSession:
    def __init__(self, bot, cache_name: str, useragent: str):
        self.bot = bot
        self.timeout = aiohttp.ClientTimeout(total=240)
        self.headers = {
                'User-Agent': useragent,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,'
                          'image/webp,image/png,image/svg+xml,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'DNT': '1',
                'Sec-GPC': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-site',
                'Sec-Fetch-User': '?1',
                'Priority': 'u=0, i',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
        }
        self.urls_expire_after = self.get_expiry_times()
        if not hasattr(self, 'allowed_methods'):
            self.allowed_methods = ("GET", "HEAD", "POST")
        if not hasattr(self, 'allowed_codes'):
            self.allowed_codes = (200, 301, 302)
        self.cache = self.create_cache_backend(cache_name)
        if hasattr(self, 'extra_headers'):
            extra_headers = getattr(self, 'extra_headers')
            self.headers.update(extra_headers)
        if hasattr(self, 'timeout'):
            self.timeout = getattr(self, 'timeout')

        self.session: CachedSession = CachedSession(cache=self.cache, headers=self.headers, timeout=self.timeout)

    def get_expiry_times(self) -> dict:
        """ Sets expiration times for different URLs. Can be overridden. """
        return {}

    def create_cache_backend(self, cache_name: str = "Default-Cache"):
        """ Abstract method to create the cache backend. Can be overridden. """
        if self.bot.config.DevelopmentConfig.test:
            return CacheBackend(
                    cache_name=cache_name,
                    urls_expire_after=self.get_expiry_times(),
                    allowed_methods=self.allowed_methods,
                    include_headers=True,
                    allowed_codes=self.allowed_codes
            )
        if self.bot.config.CacheConfig.type in [CacheType.REDIS, CacheType.VALKEY]:
            return RedisBackend(
                    cache_name=f"{self.bot.config.CacheConfig.namespace}-{cache_name}",
                    urls_expire_after=self.get_expiry_times(),
                    allowed_methods=self.allowed_methods,
                    include_headers=True,
                    allowed_codes=self.allowed_codes
            )
        else:
            return SQLiteBackend(
                    cache_name=f".cache/aiohttp-{cache_name}.db",
                    urls_expire_after=self.get_expiry_times(),
                    allowed_methods=self.allowed_methods,
                    include_headers=True,
                    allowed_codes=self.allowed_codes
            )

    async def close(self):
        await self.session.close()

    @staticmethod
    async def get_not_cached(session: CachedSession, url: str) -> CachedResponse:
        async with session.disabled():
            await asyncio.sleep(1)
            response = await session.get(url, allow_redirects=True)  # NOQA
        return response  # NOQA


class SessionsCaches:
    def __init__(self, bot):
        self.UserAgent: str = "Mozilla/5.0 (compatible; Gorenmu/2.0; +https://github.com/MrChuw/Gorenmu)"
        for name, cls in vars(self.__class__).items():
            if isinstance(cls, type) and issubclass(cls, BaseCachedSession):
                setattr(self, name, cls(bot, useragent=self.UserAgent))  # NOQA


    async def close_all_sessions(self):
        for session in vars(self).values():
            if isinstance(session, BaseCachedSession):
                await session.close()

    class AdminCachedSession(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            super().__init__(bot=bot, cache_name="Admin_requests", useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {
                    "*.mrchuw.com.br/": timedelta(days=100),
                    "im.mrchuw.com.br/api/files/*": timedelta(days=100),
                    "static-cdn.jtvnw.net/previews-ttv/*": timedelta(days=1),
            }
    AdminCachedSession: AdminCachedSession

    class NSFWCachedSession(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            super().__init__(bot=bot, cache_name="NSFW_requests", useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {
                    "https://gelbooru.com/": timedelta(hours=1),
                    "https://rule34.xxx/": timedelta(hours=1),
                    "https://tbib.org/": timedelta(hours=1),
                    "https://safebooru.org/": timedelta(hours=1),
                    "https://xbooru.com/": timedelta(hours=1),
                    "https://realbooru.com/": timedelta(hours=1),
                    "https://hypnohub.net/": timedelta(hours=1),
                    "https://danbooru.donmai.us/": timedelta(hours=1),
                    "https://booru.allthefallen.moe/": timedelta(hours=1),
                    "https://yande.re/": timedelta(hours=1),
                    "https://konachan.com/": timedelta(hours=1),
                    "https://konachan.net/": timedelta(hours=1),
                    "https://lolibooru.moe/": timedelta(hours=1),
                    "https://e621.net/": timedelta(hours=1), "https://e926.net/": timedelta(hours=1),
                    "https://derpibooru.org/": timedelta(hours=1),
                    "https://furbooru.com/": timedelta(hours=1),
                    "http://behoimi.org/": timedelta(hours=1),
                    "https://rule34.paheal.net/": timedelta(hours=1),
                }
    NSFWCachedSession: NSFWCachedSession

    class RandomCachedSession(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            super().__init__(bot=bot, cache_name="Random_requests", useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {
                    "*.imgur.com/*": timedelta(days=200),
                    "scp-wiki.wikidot.com": -1,
                    "https://pt.wikihow.com/Especial:Randomizer": 1,
                    "https://pt.wikipedia.org/wiki/Special:Random": 1,
            }
    RandomCachedSession: RandomCachedSession

    class GeneralCachedSession(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            super().__init__(bot=bot, cache_name="General_requests", useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {"*.dicio.com": timedelta(days=120)}
    GeneralCachedSession: GeneralCachedSession

    class InfoCachedSession(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            super().__init__(bot=bot, cache_name="Info_requests", useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {"*.jtvnw.net/*": timedelta(minutes=30)}
    InfoCachedSession: InfoCachedSession

    class ToolsCachedSession(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            super().__init__(bot=bot, cache_name="Tools_requests", useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {
                    "*.mrchuw.com.br/": timedelta(days=100),
                    "nominatim.openstreetmap.org/*": timedelta(days=7),
                    "api.open-meteo.com/v1/forecast": timedelta(minutes=5),
                    "https://api.mathjs.org": timedelta(days=100),
                }
    ToolsCachedSession: ToolsCachedSession

    class AliasCachedSession(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, cache_name="Alias_requests", useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {"*/*": timedelta(hours=1000)}
    AliasCachedSession: AliasCachedSession

    class CountCachedSession(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, cache_name="Count_requests", useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {"*/*": timedelta(minutes=30)}
    CountCachedSession: CountCachedSession

    class TranslateCachedSession(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, cache_name="Translate_requests", useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {"*/*": timedelta(weeks=4*6)}
    TranslateCachedSession: TranslateCachedSession

    class ImgurCachedSession(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, cache_name="Imgur_requests", useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {"*/*": timedelta(weeks=4*6)}
    ImgurCachedSession: ImgurCachedSession

    class ColorCachedSession(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, cache_name="Color_requests", useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {"thecolorapi.com": timedelta(days=30)}
    ColorCachedSession: ColorCachedSession

    class ScpCachedSession(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, cache_name="Scp_requests", useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {"scp-wiki.wikidot.com/*": timedelta(weeks=4)}
    ScpCachedSession: ScpCachedSession

    class WikihowCachedSession(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, cache_name="Wikihow_requests", useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {"*.wikihow.com/*": timedelta(weeks=4)}
    WikihowCachedSession: WikihowCachedSession

    class WikipediaCachedSession(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, cache_name="Wikipedia_requests", useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {"*.wikipedia.com/*": timedelta(weeks=4)}
    WikipediaCachedSession: WikipediaCachedSession

    class BooruCachedSession(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            self.extra_headers = {'Alt-Used': 'danbooru.donmai.us', 'TE': 'trailers'}
            self.timeout = aiohttp.ClientTimeout(total=240)
            super().__init__(bot=bot, cache_name="Booru_requests", useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {
                    self.bot.config.ApisConfig.shlink_url: timedelta(hours=24),
                    "https://gelbooru.com/": timedelta(hours=1),
                    "https://rule34.xxx/": timedelta(hours=1),
                    "https://tbib.org/": timedelta(hours=1),
                    "https://safebooru.org/": timedelta(hours=1),
                    "https://xbooru.com/": timedelta(hours=1),
                    "https://realbooru.com/": timedelta(hours=1),
                    "https://hypnohub.net/": timedelta(hours=1),
                    "https://danbooru.donmai.us/": timedelta(hours=1),
                    "https://booru.allthefallen.moe/": timedelta(hours=1),
                    "https://yande.re/": timedelta(hours=1),
                    "https://konachan.com/": timedelta(hours=1),
                    "https://konachan.net/": timedelta(hours=1),
                    "https://lolibooru.moe/": timedelta(hours=1),
                    "https://e621.net/": timedelta(hours=1),
                    "https://e926.net/": timedelta(hours=1),
                    "https://derpibooru.org/": timedelta(hours=1),
                    "https://furbooru.com/": timedelta(hours=1),
                    "http://behoimi.org/": timedelta(hours=1),
                    "https://rule34.paheal.net/": timedelta(hours=1),
                    }
    BooruCachedSession: BooruCachedSession

    class EmotesCachedSession(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            super().__init__(bot=bot, cache_name="Emotes_requests", useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {
                    "*7tv.io/v3/*": timedelta(minutes=15),
                    "*api.betterttv.net/3/*": timedelta(minutes=15),
                    "*api.frankerfacez.com/v1/*": timedelta(minutes=15),
            }
    EmotesCachedSession: EmotesCachedSession

