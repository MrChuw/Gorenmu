from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, TYPE_CHECKING

import redis
from aiocache import Cache as aioCache
from aiocache.backends.memcached import MemcachedCache
from aiocache.backends.memory import SimpleMemoryCache
from aiocache.backends.redis import RedisCache
from aiocache.serializers import PickleSerializer
from aiohttp_client_cache import CachedSession, RedisBackend, SQLiteBackend

from bot.ext.commands import Context
from bot.ext.config import CacheType
from bs4 import BeautifulSoup

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
            bot.cache = aioCache(aioCache.REDIS, serializer=PickleSerializer(), endpoint=bot.config.CacheConfig.host,
                                 port=bot.config.CacheConfig.port, namespace=bot.config.CacheConfig.namespace, )
            bot.redis = redis.Redis(host=bot.cache.endpoint, port=bot.cache.port, decode_responses=True)
        elif bot.config.CacheConfig.type == CacheType.MEMCACHED:
            bot.cache = aioCache(aioCache.MEMCACHED, serializer=PickleSerializer(), endpoint="localhost", port=11211,
                                 namespace="main"
                                 )
        else:
            bot.cache = aioCache(aioCache.MEMORY, serializer=PickleSerializer(), namespace="main")
        return bot.cache

    @staticmethod
    def create_cache() -> RedisCache | MemcachedCache | SimpleMemoryCache:
        return aioCache(aioCache.MEMORY, serializer=PickleSerializer(), namespace="main")


CODE_LIST = (200, 201, 202, 204, 301, 302, 304, 400, 401, 403, 404, 405, 408, 409, 410, 500, 501, 502, 503, 504)


class SessionsCaches:
    def __init__(self, bot):
        self.AdminCachedSession: SessionsCaches.AdminCachedSession = self.AdminCachedSession(bot)
        self.RandomCachedSession: SessionsCaches.RandomCachedSession = self.RandomCachedSession(bot)
        self.BooruCachedSession: SessionsCaches.NSFWCachedSession = self.NSFWCachedSession(bot)
        self.GeneralCachedSession: SessionsCaches.GeneralCachedSession = self.GeneralCachedSession(bot)
        self.InfoCachedSession: SessionsCaches.InfoCachedSession = self.InfoCachedSession(bot)
        self.ToolsCachedSession: SessionsCaches.ToolsCachedSession = self.ToolsCachedSession(bot)


        self.UserAgent: str = self.UserAgent(bot).user_agent
        self.AliasCachedSession: SessionsCaches.AliasCachedSession = self.AliasCachedSession(bot, self.UserAgent)
        self.CountCachedSession: SessionsCaches.CountCachedSession = self.CountCachedSession(bot, self.UserAgent)
        self.TranslateCachedSession: SessionsCaches.TranslateCachedSession = self.TranslateCachedSession(bot, self.UserAgent)
        self.ImgurCachedSession: SessionsCaches.ImgurCachedSession = self.ImgurCachedSession(bot, self.UserAgent)
        self.ColorCachedSession: SessionsCaches.ColorCachedSession = self.ColorCachedSession(bot, self.UserAgent)
        self.ScpCachedSession: SessionsCaches.ScpCachedSession = self.ScpCachedSession(bot, self.UserAgent)
        self.WikihowCachedSession: SessionsCaches.WikihowCachedSession = self.WikihowCachedSession(bot, self.UserAgent)
        self.WikipediaCachedSession: SessionsCaches.WikipediaCachedSession = self.WikipediaCachedSession(bot, self.UserAgent)

    async def close_all_sessions(self):
        for session in vars(self).values():
            if isinstance(session, CachedSession):
                await session.close()

    class AdminCachedSession:
        def __init__(self, bot: Gorenmu):
            self.bot = bot
            self.urls_expire_after = {"*.mrchuw.com.br/": timedelta(days=100),
                                      "im.mrchuw.com.br/api/files/*": timedelta(days=100),
                                      "static-cdn.jtvnw.net/previews-ttv/*": timedelta(days=1),
                                      }
            self.allowed_methods = ("GET", "HEAD", "POST")
            if "redis" in bot.__dict__:
                self.cache = RedisBackend(cache_name=f"{bot.config.CacheConfig.namespace}-Admin_requests",
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
                                      "https://e621.net/": timedelta(hours=1), "https://e926.net/": timedelta(hours=1),
                                      "https://derpibooru.org/": timedelta(hours=1),
                                      "https://furbooru.com/": timedelta(hours=1),
                                      "http://behoimi.org/": timedelta(hours=1),
                                      "https://rule34.paheal.net/": timedelta(hours=1),
                                      }
            self.allowed_methods = ("GET", "HEAD", "POST")
            if "redis" in bot.__dict__:
                self.cache = RedisBackend(cache_name=f"{bot.config.CacheConfig.namespace}-NSFW_requests",
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
                                  "Chrome/114.0.0.0 Safari/537.36"
            }
            if "redis" in bot.__dict__:
                self.cache = RedisBackend(cache_name=f"{bot.config.CacheConfig.namespace}-Random_requests",
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
                self.cache = RedisBackend(cache_name=f"{bot.config.CacheConfig.namespace}-General_requests",
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
                self.cache = RedisBackend(cache_name=f"{bot.config.CacheConfig.namespace}-Info_requests",
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
                self.cache = RedisBackend(cache_name=f"{bot.config.CacheConfig.namespace}-Tools_requests",
                                          urls_expire_after=self.urls_expire_after,
                                          allowed_methods=self.allowed_methods, include_headers=True, )
            else:
                self.cache: SQLiteBackend = SQLiteBackend(cache_name=".cache/aiohttp-tools-requests.db",
                                                          urls_expire_after=self.urls_expire_after,
                                                          allowed_methods=self.allowed_methods, include_headers=True, )
            self.session: CachedSession = CachedSession(cache=self.cache)

    class UserAgent:
        def __init__(self, bot: Gorenmu):
            self.bot = bot
            self.urls_expire_after = {"*/*": timedelta(weeks=4)}
            self.allowed_methods = ("GET", "HEAD", "POST")
            self.allowed_codes = (200,)
            if "redis" in bot.__dict__:
                self.cache = RedisBackend(cache_name=f"{bot.config.CacheConfig.namespace}-UserAgent_requests",
                                          urls_expire_after=self.urls_expire_after,
                                          allowed_methods=self.allowed_methods, include_headers=True,
                                          allowed_codes=self.allowed_codes)
            else:
                self.cache: SQLiteBackend = SQLiteBackend(cache_name=".cache/aiohttp-UserAgent-requests.db",
                                                          urls_expire_after=self.urls_expire_after,
                                                          allowed_methods=self.allowed_methods, include_headers=True,
                                                          allowed_codes=self.allowed_codes)

            self.session: CachedSession = CachedSession(cache=self.cache)
            url = 'https://www.whatismybrowser.com/guides/the-latest-user-agent/chrome'
            response = bot.loop.run_until_complete(self.session.get(url))
            text = bot.loop.run_until_complete(response.text())

            soup = BeautifulSoup(text, 'html.parser')
            chrome_td = soup.find('td', text='Chrome (Standard)')
            self.user_agent = chrome_td.find_next('span', class_='code').get_text()


    class AliasCachedSession:
        def __init__(self, bot: Gorenmu, user_agent: str):
            self.bot = bot
            self.urls_expire_after = {"*/*": timedelta(hours=1000)}
            self.allowed_methods = ("GET", "HEAD", "POST")
            self.allowed_codes = (200,)
            self.headers = {
                    'User-Agent': user_agent,
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
            if "redis" in bot.__dict__:
                self.cache = RedisBackend(cache_name=f"{bot.config.CacheConfig.namespace}-Alias_requests",
                                          urls_expire_after=self.urls_expire_after,
                                          allowed_methods=self.allowed_methods, include_headers=True,
                                          allowed_codes=self.allowed_codes)
            else:
                self.cache: SQLiteBackend = SQLiteBackend(cache_name=".cache/aiohttp-Alias-requests.db",
                                                          urls_expire_after=self.urls_expire_after,
                                                          allowed_methods=self.allowed_methods, include_headers=True,
                                                          allowed_codes=self.allowed_codes)
            self.session: CachedSession = CachedSession(cache=self.cache, headers=self.headers)

    class CountCachedSession:
        def __init__(self, bot: Gorenmu, user_agent: str):
            self.bot = bot
            self.urls_expire_after = {"*/*": timedelta(minutes=30)}
            self.allowed_methods = ("GET", "HEAD", "POST")
            self.allowed_codes = (200,)
            self.headers = {
                    'User-Agent': user_agent,
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
            if "redis" in bot.__dict__:
                self.cache = RedisBackend(cache_name=f"{bot.config.CacheConfig.namespace}-Count_requests",
                                          urls_expire_after=self.urls_expire_after,
                                          allowed_methods=self.allowed_methods, include_headers=True,
                                          allowed_codes=self.allowed_codes)
            else:
                self.cache: SQLiteBackend = SQLiteBackend(cache_name=".cache/aiohttp-Count-requests.db",
                                                          urls_expire_after=self.urls_expire_after,
                                                          allowed_methods=self.allowed_methods, include_headers=True,
                                                          allowed_codes=self.allowed_codes)
            self.session: CachedSession = CachedSession(cache=self.cache, headers=self.headers)

    class TranslateCachedSession:
        def __init__(self, bot: Gorenmu, user_agent: str):
            self.bot = bot
            self.urls_expire_after = {"*/*": timedelta(weeks=4*6)}
            self.allowed_methods = ("GET", "HEAD", "POST")
            self.allowed_codes = (200,)
            self.headers = {
                    'User-Agent': user_agent,
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
            if "redis" in bot.__dict__:
                self.cache = RedisBackend(cache_name=f"{bot.config.CacheConfig.namespace}-Translate_requests",
                                          urls_expire_after=self.urls_expire_after,
                                          allowed_methods=self.allowed_methods,
                                          include_headers=True,
                                          allowed_codes=self.allowed_codes)
            else:
                self.cache: SQLiteBackend = SQLiteBackend(cache_name=".cache/aiohttp-Translate-requests.db",
                                                          urls_expire_after=self.urls_expire_after,
                                                          allowed_methods=self.allowed_methods, include_headers=True,
                                                          allowed_codes=self.allowed_codes)
            self.session: CachedSession = CachedSession(cache=self.cache, headers=self.headers)

    class ImgurCachedSession:
        def __init__(self, bot: Gorenmu, user_agent: str):
            self.bot = bot
            self.urls_expire_after = {"*/*": timedelta(weeks=4*6)}
            self.allowed_methods = ("GET", "HEAD", "POST")
            self.allowed_codes = (200,)
            self.headers = {
                    'User-Agent': user_agent,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,'
                              'image/webp,image/png,image/svg+xml,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Referer': 'https://imgur.com/',
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
            if "redis" in bot.__dict__:
                self.cache = RedisBackend(cache_name=f"{bot.config.CacheConfig.namespace}-Imgur_requests",
                                          urls_expire_after=self.urls_expire_after,
                                          allowed_methods=self.allowed_methods,
                                          include_headers=True,
                                          allowed_codes=self.allowed_codes
                                          )
            else:
                self.cache: SQLiteBackend = SQLiteBackend(cache_name=".cache/aiohttp-Imgur-requests.db",
                                                          urls_expire_after=self.urls_expire_after,
                                                          allowed_methods=self.allowed_methods,
                                                          include_headers=True,
                                                          allowed_codes=self.allowed_codes
                                                          )
            self.session: CachedSession = CachedSession(cache=self.cache, headers=self.headers)

    class ColorCachedSession:
        def __init__(self, bot: Gorenmu, user_agent: str):
            self.bot = bot
            self.urls_expire_after = {"thecolorapi.com": timedelta(days=30)}
            self.allowed_methods = ("GET", "HEAD", "POST")
            self.allowed_codes = (200,)
            self.headers = {
                    'User-Agent': user_agent,
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
            if "redis" in bot.__dict__:
                self.cache = RedisBackend(cache_name=f"{bot.config.CacheConfig.namespace}-Color_requests",
                                          urls_expire_after=self.urls_expire_after,
                                          allowed_methods=self.allowed_methods,
                                          include_headers=True,
                                          allowed_codes=self.allowed_codes
                                          )
            else:
                self.cache: SQLiteBackend = SQLiteBackend(cache_name=".cache/aiohttp-Color-requests.db",
                                                          urls_expire_after=self.urls_expire_after,
                                                          allowed_methods=self.allowed_methods,
                                                          include_headers=True,
                                                          allowed_codes=self.allowed_codes
                                                          )
            self.session: CachedSession = CachedSession(cache=self.cache, headers=self.headers)

    class ScpCachedSession:
        def __init__(self, bot: Gorenmu, user_agent: str):
            self.bot = bot
            self.urls_expire_after = {"scp-wiki.wikidot.com/*": timedelta(weeks=4)}
            self.allowed_methods = ("GET", "HEAD", "POST")
            self.allowed_codes = (200,)
            self.headers = {
                    'User-Agent': user_agent,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,'
                              'image/svg+xml,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate, zstd',
                    'DNT': '1',
                    'Sec-GPC': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none',
                    'Sec-Fetch-User': '?1',
                    'Priority': 'u=0, i',
                }
            if "redis" in bot.__dict__:
                self.cache = RedisBackend(cache_name=f"{bot.config.CacheConfig.namespace}-Scp_requests",
                                          urls_expire_after=self.urls_expire_after,
                                          allowed_methods=self.allowed_methods,
                                          include_headers=True,
                                          allowed_codes=self.allowed_codes
                                          )
            else:
                self.cache: SQLiteBackend = SQLiteBackend(cache_name=".cache/aiohttp-Scp-requests.db",
                                                          urls_expire_after=self.urls_expire_after,
                                                          allowed_methods=self.allowed_methods,
                                                          include_headers=True,
                                                          allowed_codes=self.allowed_codes
                                                          )
            self.session: CachedSession = CachedSession(cache=self.cache, headers=self.headers)

    class WikihowCachedSession:
        def __init__(self, bot: Gorenmu, user_agent: str):
            self.bot = bot
            self.urls_expire_after = {"*.wikihow.com/*": timedelta(weeks=4)}
            self.allowed_methods = ("GET", "HEAD", "POST")
            self.allowed_codes = (200,)
            self.headers = {
                    'User-Agent': user_agent,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,'
                              'image/svg+xml,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate, zstd',
                    'DNT': '1',
                    'Sec-GPC': '1',
                    'Alt-Used': 'wikihow.com',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'cross-site',
                    'If-Modified-Since': 'Fri, 06 Sep 2024 17:26:47 GMT',
                    'Priority': 'u=0, i',
            }
            if "redis" in bot.__dict__:
                self.cache = RedisBackend(cache_name=f"{bot.config.CacheConfig.namespace}-Wikihow_requests",
                                          urls_expire_after=self.urls_expire_after,
                                          allowed_methods=self.allowed_methods,
                                          include_headers=True,
                                          allowed_codes=self.allowed_codes
                                          )
            else:
                self.cache: SQLiteBackend = SQLiteBackend(cache_name=".cache/aiohttp-Wikihow-requests.db",
                                                          urls_expire_after=self.urls_expire_after,
                                                          allowed_methods=self.allowed_methods,
                                                          include_headers=True,
                                                          allowed_codes=self.allowed_codes
                                                          )
            self.session: CachedSession = CachedSession(cache=self.cache, headers=self.headers)

    class WikipediaCachedSession:
        def __init__(self, bot: Gorenmu, user_agent: str):
            self.bot = bot
            self.urls_expire_after = {"*.wikipedia.com/*": timedelta(weeks=4)}
            self.allowed_methods = ("GET", "HEAD", "POST")
            self.allowed_codes = (200,)
            self.headers = {
                    'User-Agent': user_agent,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,'
                              'image/svg+xml,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate, zstd',
                    'DNT': '1',
                    'Sec-GPC': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none',
                    'Sec-Fetch-User': '?1',
                    'Priority': 'u=0, i',
                }
            if "redis" in bot.__dict__:
                self.cache = RedisBackend(cache_name=f"{bot.config.CacheConfig.namespace}-Wikipedia_requests",
                                          urls_expire_after=self.urls_expire_after,
                                          allowed_methods=self.allowed_methods,
                                          include_headers=True,
                                          allowed_codes=self.allowed_codes
                                          )
            else:
                self.cache: SQLiteBackend = SQLiteBackend(cache_name=".cache/aiohttp-Wikipedia-requests.db",
                                                          urls_expire_after=self.urls_expire_after,
                                                          allowed_methods=self.allowed_methods,
                                                          include_headers=True,
                                                          allowed_codes=self.allowed_codes
                                                          )
            self.session: CachedSession = CachedSession(cache=self.cache, headers=self.headers)


