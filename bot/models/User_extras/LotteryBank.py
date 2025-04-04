from __future__ import annotations

from tortoise import fields

from bot.models.base import Base, TimestampMixin


class LotteryBank(Base, TimestampMixin):
    quantity: fields.IntField = fields.IntField(default=0)
    closed_in: fields.DatetimeField = fields.DatetimeField(null=True)
    closed: fields.BooleanField = fields.BooleanField(default=False)
    accumulated: fields.BooleanField = fields.BooleanField(default=True)
    drawn_numbers: fields.JSONField = fields.JSONField(null=True)
    accumulated_quantity: fields.IntField = fields.IntField(default=0)

    users = fields.ReverseRelation["User"]

    class Meta:
        table = "lottery_bank"

    async def add(self, value: int):
        self.quantity += value
        await self.save()
