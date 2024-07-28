from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Union

from tortoise import fields

from bot.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from bot.models.User import User


class Cookies(Base, TimestampMixin):
    daily: Union[int, fields.IntField] = fields.IntField(default=datetime.now().toordinal())
    stocked: Union[float, fields.FloatField] = fields.FloatField(default=10)
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

    async def daily_update(self, value: int, quantity: int = 1) -> Cookies:
        self.daily = self.daily + quantity
        self.consumed = self.consumed + value
        self.total = self.total + value
        await self.save()
        return self

    async def donate_update(self, value: int, quantity: int = 1) -> Cookies:
        self.daily = self.daily + quantity
        self.donated = self.donated + value
        self.total = self.total + value
        await self.save()
        return self

    async def receive_update(self, value: int) -> Cookies:
        self.stocked = self.stocked + value
        self.received = self.received + value
        self.total = self.total + value
        await self.save()
        return self

    async def stock_update(self, value: int, quantity: int = 1) -> Cookies:
        self.stocked = self.stocked + value
        self.daily = self.daily + quantity
        self.total = self.total + value
        await self.save()
        return self

    async def reduce_update(self, value: int) -> Cookies:
        self.stocked = self.stocked - value
        self.total = self.total + value
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
        await self.save()
        return self
