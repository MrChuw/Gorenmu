from __future__ import annotations

from datetime import datetime
from typing import Optional

from tortoise import fields


from models.base import Base, TimestampMixin
from models.base import IntFieldInt, FloatFieldFloat
from typing import Any, List, Optional, Tuple, TYPE_CHECKING, Union
if TYPE_CHECKING:
    from models.User.User import User

class Cookies(Base, TimestampMixin):
    daily: IntFieldInt = fields.IntField(default=datetime.now().toordinal())
    stocked: FloatFieldFloat = fields.FloatField(default=10)
    streak: IntFieldInt = fields.IntField(default=0)
    comidos: IntFieldInt = fields.IntField(default=0)
    donated: IntFieldInt = fields.IntField(default=0)
    received: IntFieldInt = fields.IntField(default=0)
    total: IntFieldInt = fields.IntField(default=0)

    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="cookies"
    )

    class Meta:
        table = "cookie"

    def __getitem__(self, item):
        return getattr(self, item)

    async def daily_update(self, value: int, quantity: int = 1) -> Cookies:
        self.daily = self.daily + quantity
        self.comidos = self.comidos + value
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





























