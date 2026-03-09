from __future__ import annotations

from datetime import UTC, datetime, timedelta
from math import ceil
from typing import TYPE_CHECKING

from tortoise import fields

from bot.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from bot.ext import Context, Response, TranslationBase
    from bot.models.user import User


class Cookies(Base, TimestampMixin):
    cooldown: fields.DatetimeField = fields.DatetimeField(null=True)
    stocked: fields.IntField = fields.IntField(default=10)
    streak: fields.IntField = fields.IntField(default=0)
    consumed: fields.IntField = fields.IntField(default=0)
    donated: fields.IntField = fields.IntField(default=0)
    received: fields.IntField = fields.IntField(default=0)
    total: fields.IntField = fields.IntField(default=0)

    user: User = fields.ForeignKeyField("models.User", related_name="cookies")
    daily: fields.IntField = fields.IntField(generated=True, null=True)

    class Meta:
        table = "cookie"

    def __getitem__(self, item):
        return getattr(self, item)

    async def daily_update(self, value: int = 1) -> Cookies:
        self.cooldown = self.cooldown + timedelta(hours=6 * value)
        self.consumed = self.consumed + value
        self.total = self.total + value
        await self.save()
        return self

    async def gift_all(self, value: int, total: int) -> Cookies:
        self.cooldown = datetime.now(UTC) + timedelta(hours=6)
        if self.stocked:
            self.stocked -= value
        self.donated += total
        await self.save()
        return self

    async def gift(self, value: int, cooldown: bool = True) -> Cookies:
        if not cooldown and not self.stocked:
            self.cooldown = self.cooldown + timedelta(hours=6)
        if self.stocked:
            self.stocked -= value
        self.donated += value
        await self.save()
        return self

    async def receive_update(self, value: int) -> Cookies:
        self.stocked = self.stocked + value
        self.received = self.received + value
        self.total = self.total + value
        await self.save()
        return self

    async def stock(self, value: int) -> Cookies:
        self.cooldown = self.cooldown + (timedelta(hours=6 * value if value != 0 else 1))
        self.stocked = self.stocked + value
        self.total = self.total + value
        await self.save()
        return self

    async def stock_all(self, value: int) -> Cookies:
        self.cooldown = datetime.now(UTC) + timedelta(hours=6)
        self.stocked = self.stocked + value
        self.total = self.total + value
        await self.save()
        return self

    async def reduce_update(self, value: int) -> Cookies:
        self.stocked = self.stocked - value
        await self.save()
        return self

    async def refund_update(self, value: int) -> Cookies:
        self.stocked = self.stocked + value
        self.total = self.total - value
        await self.save()
        return self

    async def dev_give(self, value: int) -> Cookies:
        self.stocked = self.stocked + value
        self.total = self.total + value
        await self.save()
        return self

    async def lottery_update(self, value: int) -> Cookies:
        self.stocked = self.stocked + value
        self.total = self.total + value
        await self.save()
        return self

    async def new_cooldown(self, extra: int = 1) -> Cookies:
        self.cooldown = datetime.now(UTC) - timedelta(hours=6 * extra)
        await self.save()
        return self

    def not_redeemed(self) -> int:
        cookie_cooldown = datetime.now(UTC) - self.cooldown
        hours_difference = cookie_cooldown.total_seconds() / 3600
        chunk_size = 6
        return max(0, ceil(hours_difference / chunk_size))

    def datetime_to(self, amount: int):
        total_hours_needed = amount * timedelta(hours=6).total_seconds() / 3600
        final_time = self.cooldown + timedelta(hours=total_hours_needed)
        return final_time - datetime.now(UTC)  # NOQA TODO: fix NOQA?

    @staticmethod
    async def find_by_name(
        name: str, ctx: Context, translations: TranslationBase, none: bool = False
    ) -> Cookies | Response | None:
        cookie = await ctx.bot.memcache.Cookie.get_by_name(name)
        if not cookie:
            user_id = await ctx.bot.memcache.Cookie.get_id_by_name(name)
            cookie = await Cookies.get_or_none(user_id=user_id)
            if not cookie:
                return None if none else translations.Exceptions.user_not_found_name(name)
            await ctx.bot.memcache.Cookie.set(user=[cookie.id, name], cookie=cookie)
        return cookie

    @staticmethod
    async def find_by_id(
        user: User, ctx: Context, translations: TranslationBase, none: bool = False
    ) -> Cookies | Response | None:
        cookie = await ctx.bot.memcache.Cookie.get(user_id=user.id)
        if not cookie:
            cookie = await Cookies.get_or_none(id=user.id)
            if not cookie:
                return None if none else translations.Exceptions.user_not_found_id(user.id)
            await ctx.bot.memcache.Cookie.set(user=user, cookie=cookie)
        return cookie

    @staticmethod
    async def get_cookie(
        ctx: Context, translations: TranslationBase, name: str | None = None, user: User = None, none: bool = False
    ) -> Cookies | Response:
        if name:
            return await Cookies.find_by_name(name=name, ctx=ctx, translations=translations, none=none)
        elif user:
            return await Cookies.find_by_id(user=user, ctx=ctx, translations=translations, none=none)
        else:
            return await Cookies.find_by_id(user=ctx.user, ctx=ctx, translations=translations, none=none)
