from __future__ import annotations

from datetime import datetime
from typing import Union

from tortoise import fields

from bot.models.base import Base, TimestampMixin


class LotteryBank(Base, TimestampMixin):
    quantity: Union[int, fields.IntField] = fields.IntField(default=0)
    closed_in: Union[datetime, fields.DatetimeField] = fields.DatetimeField(null=True)
    closed: Union[bool, fields.BooleanField] = fields.BooleanField(default=False)
    accumulated: Union[bool, fields.BooleanField] = fields.BooleanField(default=True)
    drawn_numbers: Union[list, fields.JSONField] = fields.JSONField(null=True)
    accumulated_quantity: Union[int, fields.IntField] = fields.IntField(default=0)

    users = fields.ReverseRelation["User"]

    class Meta:
        table = "lottery_bank"

    async def add(self, value: int):
        self.quantity += value
        await self.save()
