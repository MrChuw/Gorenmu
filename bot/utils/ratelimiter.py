from __future__ import annotations

import asyncio
import threading
import time
from collections import deque
from dataclasses import dataclass, field
from types import TracebackType

from bot.utils.singleton import Singleton


@dataclass(eq=False)
class _Bucket:
    name: str
    max_calls: int = 1_000_000
    period: float = 1.0
    timestamps: deque[float] = field(default_factory=deque)
    sync_lock: threading.Lock = field(default_factory=threading.Lock)
    _async_lock: asyncio.Lock | None = None

    @property
    def async_lock(self) -> asyncio.Lock:
        lock = self._async_lock
        if lock is None:
            lock = asyncio.Lock()
            self._async_lock = lock
        return lock


class _AsyncContextManager:
    __slots__ = ("_bucket", "_limiter", "_max_calls", "_period")

    _limiter: RateLimiter
    _bucket: str
    _max_calls: int | None
    _period: float | None

    def __init__(
        self,
        limiter: RateLimiter,
        bucket: str,
        max_calls: int | None,
        period: float | None,
    ) -> None:
        self._limiter = limiter
        self._bucket = bucket
        self._max_calls = max_calls
        self._period = period

    async def __aenter__(self) -> RateLimiter:
        await self._limiter.acquire(self._bucket, max_calls=self._max_calls, period=self._period)
        return self._limiter

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        return None


class _SyncContextManager:
    __slots__ = ("_bucket", "_limiter", "_max_calls", "_period")

    _limiter: RateLimiter
    _bucket: str
    _max_calls: int | None
    _period: float | None

    def __init__(
        self,
        limiter: RateLimiter,
        bucket: str,
        max_calls: int | None,
        period: float | None,
    ) -> None:
        self._limiter = limiter
        self._bucket = bucket
        self._max_calls = max_calls
        self._period = period

    def __enter__(self) -> RateLimiter:
        self._limiter.acquire_sync(self._bucket, max_calls=self._max_calls, period=self._period)
        return self._limiter

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        return None


class RateLimiter(metaclass=Singleton):
    """Dynamic, sync/async hierarchical rate limiter."""

    _buckets: dict[str, _Bucket]
    _global_lock: threading.Lock

    def __init__(self) -> None:
        self._buckets = {}
        self._global_lock = threading.Lock()

    @staticmethod
    def _get_chain_names(bucket_path: str) -> list[str]:
        parts = [p for p in bucket_path.strip(":").split(":") if p]
        return [":".join(parts[: i + 1]) for i in range(len(parts))]

    def _get_or_create_chain(
        self,
        bucket_path: str,
        leaf_max_calls: int | None = None,
        leaf_period: float | None = None,
    ) -> list[_Bucket]:
        chain_names = self._get_chain_names(bucket_path)
        chain_nodes: list[_Bucket] = []

        with self._global_lock:
            for idx, name in enumerate(chain_names):
                if name not in self._buckets:
                    is_leaf = idx == len(chain_names) - 1
                    max_c = leaf_max_calls if (is_leaf and leaf_max_calls is not None) else 1_000_000
                    per = leaf_period if (is_leaf and leaf_period is not None) else 1.0
                    self._buckets[name] = _Bucket(name=name, max_calls=max_c, period=per)
                chain_nodes.append(self._buckets[name])

        return chain_nodes

    def configure(self, bucket_path: str, max_calls: int, period: float) -> None:
        """Dynamically configure or update limits for any node or hierarchy."""
        with self._global_lock:
            existing = self._buckets.get(bucket_path)
            if existing is None:
                self._buckets[bucket_path] = _Bucket(name=bucket_path, max_calls=max_calls, period=period)
            else:
                with existing.sync_lock:
                    existing.max_calls = max_calls
                    existing.period = period

    @staticmethod
    def _slide_window(bucket_obj: _Bucket, now: float) -> float:
        ts = bucket_obj.timestamps
        while ts and (now - ts[0]) >= bucket_obj.period:
            ts.popleft()

        if len(ts) < bucket_obj.max_calls:
            return 0.0

        return bucket_obj.period - (now - ts[0])

    async def acquire(
        self,
        bucket: str,
        max_calls: int | None = None,
        period: float | None = None,
    ) -> None:
        """Asynchronously acquire a slot across the full path hierarchy."""
        chain = self._get_or_create_chain(bucket, max_calls, period)

        while True:
            for node in chain:
                await node.async_lock.acquire()

            try:
                now = time.monotonic()
                max_wait = 0.0

                for node in chain:
                    wait = self._slide_window(node, now)
                    if wait > max_wait:
                        max_wait = wait

                if max_wait == 0.0:
                    for node in chain:
                        node.timestamps.append(now)
                    return
            finally:
                for node in reversed(chain):
                    node.async_lock.release()

            await asyncio.sleep(max(max_wait, 0.005))

    def acquire_sync(
        self,
        bucket: str,
        max_calls: int | None = None,
        period: float | None = None,
    ) -> None:
        """Synchronously acquire a slot across the full path hierarchy."""
        chain = self._get_or_create_chain(bucket, max_calls, period)

        while True:
            for node in chain:
                node.sync_lock.acquire()

            try:
                now = time.monotonic()
                max_wait = 0.0

                for node in chain:
                    wait = self._slide_window(node, now)
                    if wait > max_wait:
                        max_wait = wait

                if max_wait == 0.0:
                    for node in chain:
                        node.timestamps.append(now)
                    return
            finally:
                for node in reversed(chain):
                    node.sync_lock.release()

            time.sleep(max(max_wait, 0.005))

    def throttle(
        self,
        bucket: str,
        max_calls: int | None = None,
        period: float | None = None,
    ) -> _AsyncContextManager:
        """Context manager helper for `async with`."""
        return _AsyncContextManager(self, bucket, max_calls, period)

    def throttle_sync(
        self,
        bucket: str,
        max_calls: int | None = None,
        period: float | None = None,
    ) -> _SyncContextManager:
        """Context manager helper for synchronous `with`."""
        return _SyncContextManager(self, bucket, max_calls, period)


# USAGE EXAMPLES:

# 1. Configuration & Hierarchy Setup:
# limiter = RateLimiter()
# limiter.configure(bucket_path="irc", max_calls=20, period=30.0)
# limiter.configure(bucket_path="irc:mod", max_calls=100, period=30.0)
# limiter.configure(bucket_path="irc:remind", max_calls=10, period=0.5)
# limiter.configure(bucket_path="requests", max_calls=60, period=60.0)
# limiter.configure(bucket_path="requests:upload", max_calls=2, period=10.0)

# 2. Async usage with direct call:
# await RateLimiter().acquire("irc:remind:channel_name")

# 3. Async usage with 'async with':
# async with RateLimiter().throttle("irc:mod:remind:channel_name"):
#     await channel.send_message("remind!", bot_user)

# 4. Sync usage with direct call:
# RateLimiter().acquire_sync("requests:upload")
# requests.post("https://api.example.com/upload", files=data)

# 5. Sync usage with 'with':
# with RateLimiter().throttle_sync("requests:short", max_calls=5, period=1.0):
#     response = requests.get("https://api.example.com/data")

# 6. Changing configuration dynamically at runtime (e.g. Bot becomes mod in a channel):
# is_mod = True
# if is_mod:
#     RateLimiter().configure("irc", max_calls=100, period=30.0)
# else:
#     RateLimiter().configure("irc", max_calls=20, period=30.0)
