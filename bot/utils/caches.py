from __future__ import annotations

from collections.abc import Iterable
from datetime import timedelta
from typing import TYPE_CHECKING, Any

import redis
from aiocache import Cache as aioCache
from aiocache.backends.memcached import MemcachedCache
from aiocache.backends.memory import SimpleMemoryCache
from aiocache.backends.redis import RedisCache
from aiocache.serializers import PickleSerializer
from twitchio import ChannelInfo as ChannelTmi
from twitchio import User as UserTmi

from bot.ext.named_tuples import AliasCached, RAfkNamedTuple
from bot.models import Cookies as CookiesDB
from bot.models import Status
from bot.models import User as UserDB
from bot.models.Others.alias import Alias
from bot.utils.caches_base import MemoryCacheCore
from bot.utils.config import CacheType

if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.ext import Context

CODE_LIST = (200, 201, 202, 204, 301, 302, 304, 400, 401, 403, 404, 405, 408, 409, 410, 500, 501, 502, 503, 504)

__all__ = ("Cache", "MemCache", "aioCache")


class Cache:
    @staticmethod
    def cache_load(bot: Gorenmu) -> RedisCache | MemcachedCache | SimpleMemoryCache:
        if bot.config.CacheConfig.type in [CacheType.REDIS, CacheType.VALKEY]:
            bot.cache = aioCache(
                aioCache.REDIS,
                serializer=PickleSerializer(),
                endpoint=bot.config.CacheConfig.host,
                port=bot.config.CacheConfig.port,
                namespace=bot.config.CacheConfig.namespace,
            )
            bot.redis = redis.Redis(host=bot.cache.endpoint, port=bot.cache.port, decode_responses=True)
        elif bot.config.CacheConfig.type == CacheType.MEMCACHED:
            bot.cache = aioCache(
                aioCache.MEMCACHED,
                serializer=PickleSerializer(),
                endpoint="localhost",
                port=11211,
                namespace=bot.config.CacheConfig.namespace,
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
            if isinstance(cls, type) and issubclass(cls, MemoryCacheCore):
                setattr(self, name, cls())

    async def close_all_caches(self):
        for session in vars(self).values():
            if isinstance(session, MemoryCacheCore):
                await session.close()

    class Alias(MemoryCacheCore):
        def __init__(self) -> None:
            super().__init__(ttl=timedelta(hours=12))

        async def set(self, name: str, user_id: int, to_cache: AliasCached) -> None:
            await self._set(key=name, value=to_cache, namespace=user_id)

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

    class User(MemoryCacheCore):
        def __init__(self) -> None:
            super().__init__(ttl=timedelta(hours=6))

        async def set(self, user: UserDB, ttl: float | None = None) -> None:
            await self._set_map(key=str(user.id), value=user, ttl=ttl, name=user.name, user_id=user.id)

        async def get(self, user_id: int) -> UserDB | None:
            return await self._get(str(user_id))

        async def get_by_name(self, name: str) -> UserDB | None:
            return await self._get_by_name(name)

        async def list(self) -> list[UserDB]:
            return await self._list_name()

    User: User

    class Cookie(MemoryCacheCore):
        def __init__(self) -> None:
            super().__init__(ttl=timedelta(hours=16))

        async def set(self, user: UserDB | list, cookie: CookiesDB, ttl: float | None = None) -> None:
            user_id, user_name = (user[0], user[1]) if isinstance(user, list) else (user.id, user.name)
            await self._set_map(key=str(user_id), value=cookie, ttl=ttl, name=user_name, user_id=user_id)

        async def get(self, user_id: int) -> CookiesDB | None:
            return await self._get(key=str(user_id))

        async def get_by_name(self, name: str) -> CookiesDB | None:
            return await self._get_by_name(name)

        async def get_id_by_name(self, name: str) -> int | None:
            return self._get_id_by_name(name)

        async def list(self) -> list[CookiesDB]:
            return await self._list_name()

    Cookie: Cookie

    class Afk(MemoryCacheCore):
        def __init__(self):
            super().__init__(ttl=timedelta(hours=12))

        async def set(self, user: UserDB, value: Status, ttl: float | None = None) -> None:
            await self._set_map(key=str(user.id), value=value, ttl=ttl, name=user.name, user_id=user.id)

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

    class RAfk(MemoryCacheCore):
        def __init__(self):
            super().__init__(ttl=timedelta(minutes=4))

        async def set(self, user: UserDB | list, value: RAfkNamedTuple, ttl: float | None = None) -> None:
            user_id, user_name = (user[0], user[1]) if isinstance(user, list) else (user.id, user.name)
            await self._set_map(key=str(user_id), value=value, ttl=ttl, name=user_name, user_id=user_id)

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

    class UserTmi(MemoryCacheCore):
        def __init__(self):
            super().__init__(ttl=timedelta(minutes=5))

        async def set(self, name: str, to_cache: UserTmi) -> None:
            await self._set(key=name, value=to_cache)

        async def get(self, key: str) -> UserTmi:
            return await self._get(key=key)

        async def cached_or_get(self, ctx: Context, name: str | None = None, user_id: str | int | None = None):
            cached = await self.get(key=name)
            if cached:
                return cached
            user_tmi: UserTmi = await ctx.bot.fetch_user(login=name) if name else await ctx.bot.fetch_user(id=user_id)
            if not user_tmi:
                return None
            await self.set(name=name, to_cache=user_tmi)
            return user_tmi

    UserTmi: UserTmi

    class ChannelTmi(MemoryCacheCore):
        def __init__(self):
            super().__init__(ttl=timedelta(minutes=5))

        async def set(self, user_id: str | int, to_cache: ChannelTmi) -> None:
            await self._set(key=user_id, value=to_cache)

        async def get(self, user_id: str | int) -> ChannelTmi:
            return await self._get(key=user_id)

        async def cached_or_get(self, ctx: Context, user_id: str | int):
            cached = await self.get(user_id=user_id)
            if cached:
                return cached
            channel_tmi = await ctx.bot.fetch_channel(broadcaster_id=user_id)
            if not channel_tmi:
                return None
            await self.set(user_id=user_id, to_cache=channel_tmi)
            return channel_tmi

    ChannelTmi: ChannelTmi
