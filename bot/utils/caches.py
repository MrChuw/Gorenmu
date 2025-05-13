# -*- coding: utf-8 -*-
from __future__ import annotations

from datetime import timedelta
from typing import Any, Iterable, TYPE_CHECKING

import redis
from aiocache import Cache as aioCache
from aiocache.backends.memcached import MemcachedCache
from aiocache.backends.memory import SimpleMemoryCache
from aiocache.backends.redis import RedisCache
from aiocache.serializers import PickleSerializer

from bot.ext.config import CacheType
import aiohttp

from bot.ext.named_tuples import AliasCached, RAfkNamedTuple
from bot.models import Cookies as CookiesDB, Status, User as UserDB
from bot.models.Others.Alias import Alias

from bot.utils.caches_base import BaseCachedSession, BaseCacheFunctions

if TYPE_CHECKING:
    from bot.bot import Gorenmu

CODE_LIST = (200, 201, 202, 204, 301, 302, 304, 400, 401, 403, 404, 405, 408, 409, 410, 500, 501, 502, 503, 504)

__all__ = ("SessionsCaches", "Cache", "aioCache", "MemCache")


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


class MemCache:
    def __init__(self):
        for name, cls in vars(self.__class__).items():
            if isinstance(cls, type) and issubclass(cls, BaseCacheFunctions):
                setattr(self, name, cls())

    async def close_all_caches(self):
        for session in vars(self).values():
            if isinstance(session, BaseCacheFunctions):
                await session.close()

    class Alias(BaseCacheFunctions):
        def __init__(self) -> None:
            super().__init__(ttl=timedelta(hours=12))

        async def set(self, name: str, user_id: int, cached: AliasCached) -> None:
            await self._set(key=name, value=cached, namespace=user_id)

        async def get(self, key: str, user_id: int) -> AliasCached:
            return await self._get(key=key, namespace=user_id)

        async def list_keys(self, user_id: int) -> list[str]:
            return list(self.key_index.get(str(user_id), set()))

        async def list(self, user_id: int) -> list[Alias]:
            items = await self._list_key(str(user_id))
            return [item.alias for item in items if item]

        async def multi_set(self, pairs: Iterable[tuple[str, Any]], user_id: int) -> None:
            await self._multi_set(items=pairs, namespace=user_id)
    Alias: Alias

    class User(BaseCacheFunctions):
        def __init__(self) -> None:
            super().__init__(ttl=timedelta(hours=6))

        async def set(self, user: UserDB, ttl: float = None) -> None:
            await self._set(str(user.id), user, ttl)
            self._map_name(user.name, user.id)

        async def get(self, user_id: int) -> UserDB | None:
            return await self._get(str(user_id))

        async def get_by_name(self, name: str) -> UserDB | None:
            return await self._get_by_name(name)

        async def list(self) -> list[UserDB]:
            return await self._list_name()
    User: User

    class Cookie(BaseCacheFunctions):
        def __init__(self) -> None:
            super().__init__(ttl=timedelta(hours=16))

        async def set(self, user: UserDB | list, cookie: CookiesDB, ttl: float = None) -> None:
            user_id, user_name = (user[0], user[1]) if isinstance(user, list) else (user.id, user.name)
            await self._set(key=str(user_id), value=cookie, ttl=ttl)
            self._map_name(user_name, user_id)

        async def get(self, user_id: int) -> CookiesDB | None:
            return await self._get(key=str(user_id))

        async def get_by_name(self, name: str) -> CookiesDB | None:
            return await self._get_by_name(name)

        async def get_id_by_name(self, name: str) -> int | None:
            return self._get_id_by_name(name)

        async def list(self) -> list[CookiesDB]:
            return await self._list_name()
    Cookie: Cookie

    class Afk(BaseCacheFunctions):
        def __init__(self):
            super().__init__(ttl=timedelta(hours=12))

        async def set(self, user: UserDB, value: Status, ttl: float = None) -> None:
            await self._set(key=str(user.id), value=value, ttl=ttl)
            self._map_name(user.name, user.id)

        async def get(self, user_id: int) -> Status | None:
            return await self._get(key=str(user_id))

        async def get_by_name(self, name: str) -> Status | None:
            return await self._get_by_name(name)

        async def list(self) -> list[Status]:
            return await self._list_name()

        async def delete(self, user_id: int) -> None:
            await self._delete(key=str(user_id))
            self.name_to_user_id.pop(str(user_id), None)
    Afk: Afk

    class RAfk(BaseCacheFunctions):
        def __init__(self):
            super().__init__(ttl=timedelta(minutes=4))

        async def set(self, user: UserDB | list, value: RAfkNamedTuple, ttl: float = None) -> None:
            user_id, user_name = (user[0], user[1]) if isinstance(user, list) else (user.id, user.name)
            await self._set(key=str(user_id), value=value, ttl=ttl)
            self._map_name(user_name, user_id)

        async def get(self, user_id: int) -> RAfkNamedTuple | None:
            return await self._get(key=str(user_id))

        async def get_by_name(self, name: str) -> RAfkNamedTuple | None:
            return await self._get_by_name(name)

        async def list(self) -> list[RAfkNamedTuple]:
            return await self._list_name()

        async def delete(self, user_id: int) -> None:
            await self._delete(key=str(user_id))
            self.name_to_user_id.pop(str(user_id), None)
    RAfk: RAfk




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
            return {"*/*": -1}
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
