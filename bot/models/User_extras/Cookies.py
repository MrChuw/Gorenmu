from __future__ import annotations

from datetime import datetime, UTC, timedelta
from typing import TYPE_CHECKING, Union
from math import ceil

from tortoise import fields

from bot.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from bot.models.User import User


class Cookies(Base, TimestampMixin):
    cooldown: Union[datetime, fields.DatetimeField] = fields.DatetimeField(null=True)
    stocked: Union[float, fields.IntField] = fields.IntField(default=10)
    streak: Union[int, fields.IntField] = fields.IntField(default=0)
    consumed: Union[int, fields.IntField] = fields.IntField(default=0)
    donated: Union[int, fields.IntField] = fields.IntField(default=0)
    received: Union[int, fields.IntField] = fields.IntField(default=0)
    total: Union[int, fields.IntField] = fields.IntField(default=0)

    user: User = fields.ForeignKeyField("models.User", related_name="cookies")

    class Meta:
        table = "cookie"

    def __getitem__(self, item):
        return getattr(self, item)

    async def daily_update(self, value: int = 1) -> Cookies:
        self.cooldown = self.cooldown + timedelta(hours=6)
        self.consumed = self.consumed + value
        self.total = self.total + value
        await self.save()
        return self

    async def gift_all(self, value: int, cooldown: bool = True) -> Cookies:
        if not cooldown:
            self.cooldown = datetime.now(UTC) + timedelta(hours=6)
        if self.stocked:
            self.stocked -= value
        self.donated += value
        await self.save()
        return self

    async def gift(self, value: int, cooldown: bool = True) -> Cookies:
        if not cooldown and not self.stocked:
            self.cooldown = self.cooldown + timedelta(hours=6)
        if self.stocked:
            self.stocked -= 1
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
        self.cooldown = self.cooldown + (timedelta(hours=6) * value)
        self.stocked = self.stocked + value
        self.total = self.total + value
        await self.save()
        return self

    async def stock_all(self, value: int) -> Cookies:
        self.cooldown = self.cooldown = datetime.now(UTC) + timedelta(hours=6)
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


    async def new_cooldown(self) -> Cookies:
        self.cooldown = datetime.now(UTC) - timedelta(hours=6)
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
        return final_time - datetime.now(UTC)

