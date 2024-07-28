from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, TYPE_CHECKING

import redis
from aiocache import Cache
from aiocache.backends.memcached import MemcachedCache
from aiocache.backends.memory import SimpleMemoryCache
from aiocache.backends.redis import RedisCache
from aiocache.serializers import PickleSerializer
from aiohttp_client_cache import CachedSession, RedisBackend, SQLiteBackend

from bot.ext.commands import Context
from bot.ext.config import CacheType

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class Cache:
    class UserCache:
        def __init__(self, ctx: Context) -> None:
            self.badges: Dict[str, Any] = ctx.author.badges or {}
            self.color: str = ctx.author.color or None
            self.colour: str = ctx.author.colour or None
            self.display_name: str = ctx.author.display_name or None
            self.id: int = int(ctx.author.id) or None
            self.is_broadcaster: bool = ctx.author.is_broadcaster or False
            self.is_mod: bool = ctx.author.is_mod or False
            self.is_subscriber: bool = ctx.author.is_subscriber or False
            self.is_turbo: bool = ctx.author.is_turbo or False
            self.is_vip: bool = ctx.author.is_vip or False
            self.mention: str = ctx.author.mention or None
            self.name: str = ctx.author.name or None
            self.prediction: Any = ctx.author.prediction or None
            self.last_channel: str = ctx.channel.name or None
            self.last_message: str = ctx.message.content or None
            self.first_message: bool = ctx.message.first or False
            self.last_message_time: datetime = ctx.message.timestamp or None

    @staticmethod
    def cache_load(bot: Gorenmu) -> RedisCache | MemcachedCache | SimpleMemoryCache:
        if bot.config.CacheConfig.type in [CacheType.REDIS, CacheType.VALKEY]:
            bot.cache = Cache(Cache.REDIS, serializer=PickleSerializer(), endpoint=bot.config.CacheConfig.host,
                              port=bot.config.CacheConfig.port, namespace=bot.config.CacheConfig.namespace, )
            bot.redis = redis.Redis(host=bot.cache.endpoint, port=bot.cache.port, decode_responses=True)
        elif bot.config.CacheConfig.type == CacheType.MEMCACHED:
            bot.cache = Cache(Cache.MEMCACHED, serializer=PickleSerializer(), endpoint="localhost", port=11211,
                              namespace="main"
                              )
        else:
            bot.cache = Cache(Cache.MEMORY, serializer=PickleSerializer(), namespace="main")
        return bot.cache


CODE_LIST = (200, 201, 202, 204, 301, 302, 304, 400, 401, 403, 404, 405, 408, 409, 410, 500, 501, 502, 503, 504)


class SessionsCaches:
    def __init__(self, bot):
        self.AdminCachedSession: SessionsCaches.AdminCachedSession = self.AdminCachedSession(bot)
        self.RandomCachedSession: SessionsCaches.RandomCachedSession = self.RandomCachedSession(bot)
        self.BooruCachedSession: SessionsCaches.NSFWCachedSession = self.NSFWCachedSession(bot)
        self.GeneralCachedSession: SessionsCaches.GeneralCachedSession = self.GeneralCachedSession(bot)
        self.InfoCachedSession: SessionsCaches.InfoCachedSession = self.InfoCachedSession(bot)
        self.ToolsCachedSession: SessionsCaches.ToolsCachedSession = self.ToolsCachedSession(bot)

    class AdminCachedSession:
        def __init__(self, bot: Gorenmu):
            self.bot = bot
            self.urls_expire_after = {"*.mrchuw.com.br/": timedelta(days=100),
                                      "im.mrchuw.com.br/api/files/*": timedelta(days=100),
                                      "static-cdn.jtvnw.net/previews-ttv/*": timedelta(days=1),
                                      }
            self.allowed_methods = ("GET", "HEAD", "POST")
            if "redis" in bot.__dict__:
                self.cache = RedisBackend(cache_name=bot.config.CacheConfig.admin_namespace,
                                          urls_expire_after=self.urls_expire_after,
                                          allowed_methods=self.allowed_methods, include_headers=True, )
            else:
                self.cache: SQLiteBackend = SQLiteBackend(cache_name=".cache/aiohttp-admin-requests.db",
                                                          urls_expire_after=self.urls_expire_after,
                                                          allowed_methods=self.allowed_methods, include_headers=True, )

            self.session: CachedSession = CachedSession(cache=self.cache)

    class NSFWCachedSession:
        def __init__(self, bot: Gorenmu):
            self.bot = bot
            self.urls_expire_after = {"https://gelbooru.com/": timedelta(hours=1),
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
            self.allowed_methods = ("GET", "HEAD", "POST")
            if "redis" in bot.__dict__:
                self.cache = RedisBackend(cache_name=bot.config.CacheConfig.booru_namespace,
                                          urls_expire_after=self.urls_expire_after,
                                          allowed_methods=self.allowed_methods, include_headers=True, )
            else:
                self.cache: SQLiteBackend = SQLiteBackend(cache_name=".cache/aiohttp-booru-requests.db",
                                                          urls_expire_after=self.urls_expire_after,
                                                          allowed_methods=self.allowed_methods, include_headers=True, )

            self.session: CachedSession = CachedSession(cache=self.cache)

    class RandomCachedSession:
        def __init__(self, bot: Gorenmu):
            self.bot = bot
            self.urls_expire_after = {"*.imgur.com/*": timedelta(days=200), "scp-wiki.wikidot.com": -1,
                                      "https://pt.wikihow.com/Especial:Randomizer": 1,
                                      "https://pt.wikipedia.org/wiki/Special:Random": 1,
                                      }
            self.allowed_methods = ("GET", "HEAD", "POST")
            self.allowed_codes = (200, 301, 302)
            self.headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                  "Chrome/114.0.0.0 Safari/537.36"}
            if "redis" in bot.__dict__:
                self.cache = RedisBackend(cache_name=bot.config.CacheConfig.random_namespace,
                                          urls_expire_after=self.urls_expire_after,
                                          allowed_methods=self.allowed_methods, include_headers=True, )
            else:
                self.cache: SQLiteBackend = SQLiteBackend(cache_name=".cache/aiohttp-random-requests.db",
                                                          urls_expire_after=self.urls_expire_after,
                                                          allowed_codes=self.allowed_codes, headers=self.headers, )

            self.session: CachedSession = CachedSession(cache=self.cache, headers=self.headers)

    class GeneralCachedSession:
        def __init__(self, bot: Gorenmu):
            self.bot = bot
            self.urls_expire_after = {"*.jtvnw.net": timedelta(minutes=30), "*.dicio.com": timedelta(days=120)}
            self.allowed_methods = ("GET", "HEAD", "POST")
            self.allowed_codes = CODE_LIST
            if "redis" in bot.__dict__:
                self.cache = RedisBackend(cache_name=bot.config.CacheConfig.general_namespace,
                                          urls_expire_after=self.urls_expire_after,
                                          allowed_methods=self.allowed_methods, allowed_codes=self.allowed_codes,
                                          include_headers=True, )
            else:
                self.cache: SQLiteBackend = SQLiteBackend(cache_name=".cache/aiohttp-general-requests.db",
                                                          urls_expire_after=self.urls_expire_after,
                                                          allowed_methods=self.allowed_methods, include_headers=True, )
            self.session: CachedSession = CachedSession(cache=self.cache)

    class InfoCachedSession:
        def __init__(self, bot: Gorenmu):
            self.bot = bot
            self.urls_expire_after = {"*.jtvnw.net": timedelta(minutes=30)}
            self.allowed_methods = ("GET", "HEAD", "POST")
            if "redis" in bot.__dict__:
                self.cache = RedisBackend(cache_name=bot.config.CacheConfig.info_namespace,
                                          urls_expire_after=self.urls_expire_after,
                                          allowed_methods=self.allowed_methods, include_headers=True, )
            else:
                self.cache: SQLiteBackend = SQLiteBackend(cache_name=".cache/aiohttp-info-requests.db",
                                                          urls_expire_after=self.urls_expire_after,
                                                          allowed_methods=self.allowed_methods, include_headers=True, )
            self.session: CachedSession = CachedSession(cache=self.cache)

    class ToolsCachedSession:
        def __init__(self, bot: Gorenmu):
            self.bot = bot
            self.urls_expire_after = {"*.mrchuw.com.br/": timedelta(days=100),
                                      "nominatim.openstreetmap.org/*": timedelta(days=7),
                                      "api.open-meteo.com/v1/forecast": timedelta(minutes=5),
                                      "https://api.mathjs.org": timedelta(days=100),
                                      }
            self.allowed_methods = ("GET", "HEAD", "POST")
            if "redis" in bot.__dict__:
                self.cache = RedisBackend(cache_name=bot.config.CacheConfig.tools_namespace,
                                          urls_expire_after=self.urls_expire_after,
                                          allowed_methods=self.allowed_methods, include_headers=True, )
            else:
                self.cache: SQLiteBackend = SQLiteBackend(cache_name=".cache/aiohttp-tools-requests.db",
                                                          urls_expire_after=self.urls_expire_after,
                                                          allowed_methods=self.allowed_methods, include_headers=True, )
            self.session: CachedSession = CachedSession(cache=self.cache)
