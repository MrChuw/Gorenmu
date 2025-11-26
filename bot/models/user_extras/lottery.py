from __future__ import annotations

from typing import TYPE_CHECKING

from tortoise import fields

from bot.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from bot.models import LotteryBank, User


class Lottery(Base, TimestampMixin):
    bet_value: fields.IntField = fields.IntField(default=0)
    numbers: fields.JSONField = fields.JSONField(null=True)
    closed: fields.BooleanField = fields.BooleanField(default=False)
    earned: fields.IntField = fields.IntField(default=0, null=True)
    closed_in: fields.DatetimeField = fields.DatetimeField(null=True)
    draw_sorted_numbers: fields.JSONField = fields.JSONField(null=True)

    draw: LotteryBank = fields.ForeignKeyField("models.LotteryBank", related_name="User")
    user: User = fields.ForeignKeyField("models.User", related_name="Lottery")

    class Meta:
        table = "lottery"
