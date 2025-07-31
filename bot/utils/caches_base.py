# -*- coding: utf-8 -*-
from __future__ import annotations

import asyncio
import contextlib
import heapq
import time
from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Any, Callable, Iterable, Tuple

import aiohttp
from aiocache import Cache as aioCache, SimpleMemoryCache
from aiohttp_client_cache import CacheBackend, CachedResponse, CachedSession, RedisBackend, SQLiteBackend

from bot.utils.config import CacheType


class BaseCacheFunctions:
    def __init__(self, ttl: timedelta = timedelta(hours=12)):
        self.cache: SimpleMemoryCache = aioCache(aioCache.MEMORY)
        self.name_to_user_id: dict[str, int] = {}
        self.key_index: dict[str, set[str]] = {}
        self.ttl: float = ttl.total_seconds()
        self._scheduler = ExpiryScheduler(self._expire_callback)

    def _expire_callback(self, key: str, namespace: str):
        # remove do key index
        if namespace in self.key_index:
            self.key_index[namespace].discard(key)
        # remove de name_to_user_id se for um user_id
        try:
            uid = int(key)
        except ValueError:
            return
        for name, mapped in list(self.name_to_user_id.items()):
            if mapped == uid:
                del self.name_to_user_id[name]

    async def _set(self, key: str, value, ttl: float = None, namespace: str | int = "") -> None:
        ns = str(namespace)
        lifespan = ttl or self.ttl
        await self.cache.set(key=key, value=value, ttl=lifespan, namespace=ns)
        if ns:
            self.key_index.setdefault(ns, set()).add(key)
        self._scheduler.schedule(key, ns, lifespan)

    async def _multi_set(self, items: Iterable[tuple[str, Any]], ttl: float = None, namespace: str | int = "") -> None:
        ns = str(namespace)
        lifespan = ttl or self.ttl
        await self.cache.multi_set(pairs=items, ttl=lifespan, namespace=ns)
        if ns:
            self.key_index.setdefault(ns, set()).update(k for k, _ in items)
        for key, _ in items:
            self._scheduler.schedule(key, ns, lifespan)

    async def _get(self, key: str, namespace: str | int = ""):
        namespace = namespace if isinstance(namespace, str) else str(namespace)
        return await self.cache.get(key=key, namespace=namespace)

    async def _multi_get(self, keys: Iterable[str], namespace: str | int = "") -> list[Any | None]:
        namespace = namespace if isinstance(namespace, str) else str(namespace)
        return await self.cache.multi_get(keys=keys, namespace=namespace)

    async def _delete(self, key: str, namespace: str | int = "") -> None:
        namespace = namespace if isinstance(namespace, str) else str(namespace)
        await self.cache.delete(key=key, namespace=namespace)
        if namespace in self.key_index:
            self.key_index[namespace].discard(key)

    def _map_name(self, name: str, user_id: int) -> None:
        self.name_to_user_id[name] = user_id

    def _get_id_by_name(self, name: str) -> int | None:
        return self.name_to_user_id.get(name)

    async def _get_by_name(self, name: str, namespace: str | int = ""):
        namespace = namespace if isinstance(namespace, str) else str(namespace)
        user_id = self._get_id_by_name(name)
        return None if user_id is None else await self._get(str(user_id), namespace=namespace)

    async def _list_name(self):
        return [v for uid in self.name_to_user_id.values() if (v := await self._get(str(uid)))]

    async def _list_key(self, namespace: str) -> list:
        keys = list(self.key_index.get(namespace, set()))
        return [await self._get(k, namespace=namespace) for k in keys]

    async def close(self):
        await self._scheduler.close()


class BaseCachedSession(ABC):
    def __init__(self, bot, cache_name: str, useragent: str):
        self.bot = bot
        self.upload_url = self.bot.config.ApisConfig.file_upload_url / "*"
        self.shortener_url = self.bot.config.ApisConfig.shlink_url / "*"
        self.alias_url = self.bot.config.ApisConfig.alias_url / "*"

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

    @abstractmethod
    def get_expiry_times(self) -> dict:
        """Must be implemented by subclasses to set URL expiration times."""
        pass

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
            await asyncio.sleep(0.2)
            response = await session.get(url, allow_redirects=True)
        return response  # NOQA


class ExpiryScheduler:
    def __init__(self, on_expire: Callable[[str, str], None]):
        self._heap: list[Tuple[float, str, str]] = []
        self._wakeup = asyncio.Event()
        self._on_expire = on_expire
        self._task = asyncio.create_task(self._loop())

    def schedule(self, key: str, namespace: str, ttl: float):
        expire_at = time.monotonic() + ttl
        heapq.heappush(self._heap, (expire_at, namespace, key))
        if self._heap[0][0] == expire_at:
            self._wakeup.set()

    async def _loop(self):
        while True:
            if not self._heap:
                self._wakeup.clear()
                await self._wakeup.wait()
                continue

            expire_at, namespace, key = self._heap[0]
            now = time.monotonic()
            delay = expire_at - now
            if delay > 0:
                with contextlib.suppress(asyncio.TimeoutError):
                    self._wakeup.clear()
                    await asyncio.wait_for(self._wakeup.wait(), timeout=delay)
                    continue
            while self._heap and self._heap[0][0] <= time.monotonic():
                _, ns, k = heapq.heappop(self._heap)
                self._on_expire(k, ns)

    async def close(self):
        self._task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await self._task
