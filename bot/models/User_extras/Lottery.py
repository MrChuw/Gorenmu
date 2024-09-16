from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Union

from tortoise import fields

from bot.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from bot.models import User
    from bot.models import LotteryBank


class Lottery(Base, TimestampMixin):
    bet_value: Union[int, fields.IntField] = fields.IntField(default=0)
    numbers: Union[list, fields.JSONField] = fields.JSONField(null=True)
    closed: Union[bool, fields.BooleanField] = fields.BooleanField(default=False)
    earned: Union[int, fields.IntField] = fields.IntField(default=0, null=True)
    closed_in: Union[datetime, fields.DatetimeField] = fields.DatetimeField(null=True)
    draw_sorted_numbers: Union[list, fields.JSONField] = fields.JSONField(null=True)

    draw: LotteryBank = fields.ForeignKeyField('models.LotteryBank', related_name="User")
    user: User = fields.ForeignKeyField("models.User", related_name="Lottery")

    class Meta:
        table = "lottery"
