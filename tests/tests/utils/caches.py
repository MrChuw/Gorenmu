import asyncio
from collections import namedtuple
from datetime import timedelta

import pytest

from bot.utils.caches import MemCache
from bot.utils.caches_base import BaseCacheFunctions, ExpiryScheduler


@pytest.fixture
async def memcache():
    cache = MemCache()
    yield cache
    await cache.close_all_caches()


class DummyCache(BaseCacheFunctions):
    def __init__(self, ttl=timedelta(seconds=1)):
        super().__init__(ttl=ttl)

    async def set(self, key, value, ttl=None):
        await self._set(key=key, value=value, ttl=ttl)

    async def get(self, key):
        return await self._get(key)


@pytest.mark.asyncio
@pytest.mark.parametrize("value", [None, 123, "abc", {"a": 1}])
async def test_base_set_get_delete(value):
    dummy = DummyCache(ttl=timedelta(seconds=0.1))
    await dummy.set("k", value)
    assert await dummy.get("k") == value
    await dummy._delete("k")
    assert await dummy.get("k") is None
    await dummy.close()


@pytest.mark.asyncio
async def test_base_expiry():
    expired = []

    def collect(key, namespace):
        expired.append((key, namespace))

    scheduler = ExpiryScheduler(on_expire=collect)
    scheduler.schedule("x", "", ttl=0.05)
    await asyncio.sleep(0.06)
    assert ("x", "") in expired
    await scheduler.close()


@pytest.mark.asyncio
async def test_memcache_alias(memcache):
    alias = memcache.Alias
    await alias.set(name="nick", user_id=1, cached=object())  # NOQA
    keys = await alias.list_keys(user_id=1)
    assert "nick" in keys


@pytest.mark.asyncio
async def test_memcache_user(memcache):
    mem_user = memcache.User

    class FakeUser:
        def __init__(self, user_id, name):
            self.id, self.name = user_id, name

    user = FakeUser(10, "test")
    await mem_user.set(user)  # NOQA
    fetched = await mem_user.get(10)
    assert fetched == user
    by_name = await mem_user.get_by_name("test")
    assert by_name == user
    lst = await mem_user.list()
    assert user in lst


@pytest.mark.asyncio
async def test_memcache_cookie(memcache):
    mem_cookie = memcache.Cookie

    class FakeUser:
        def __init__(self, user_id, name):
            self.id, self.name = user_id, name

    Cookies = namedtuple("Cookies", ["data"])
    user = FakeUser(20, "cookie_user")
    cookie = Cookies(data="val")
    await mem_cookie.set(user, cookie)  # NOQA
    assert await mem_cookie.get(20) == cookie
    assert await mem_cookie.get_by_name("cookie_user") == cookie
    assert await mem_cookie.get_id_by_name("cookie_user") == 20


@pytest.mark.asyncio
async def test_memcache_afk_rafk(memcache):
    mem_afk = memcache.Afk
    mem_rafk = memcache.RAfk

    class FakeUser:
        def __init__(self, user_id, name):
            self.id, self.name = user_id, name

    Status = namedtuple("Status", ["msg"])
    RStatus = namedtuple("RStatus", ["msg"])
    user = FakeUser(30, "temp")
    afk = Status(msg="away")
    rafk = RStatus(msg="brb")
    await mem_afk.set(user, afk)  # NOQA
    assert await mem_afk.get(30) == afk
    assert await mem_afk.get_by_name("temp") == afk
    await mem_afk.delete(30)
    assert await mem_afk.get(30) is None
    # RAfk
    await mem_rafk.set(user, rafk)  # NOQA
    assert await mem_rafk.get(30) == rafk
    assert await mem_rafk.get_by_name("temp") == rafk
    await mem_rafk.delete(30)
    assert await mem_rafk.get(30) is None
