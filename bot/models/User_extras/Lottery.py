from __future__ import annotations

from datetime import datetime

import pytz
from tortoise import fields

from bot.models.base import Base, TimestampMixin


from typing import TYPE_CHECKING, Union


if TYPE_CHECKING:
    from bot.bot import Context
    from bot.models.User import User

class Lottery(Base, TimestampMixin):
    bet_value: Union[int, fields.IntField] = fields.IntField(default=0)
    numbers: Union[list, fields.JSONField] = fields.JSONField(null=True)
    closed: Union[bool, fields.BooleanField] = fields.BooleanField(default=False)
    earned: Union[int, fields.IntField] = fields.IntField(default=0, null=True)
    closed_in: Union[datetime, fields.DatetimeField] = fields.DatetimeField(null=True)
    draw_id: Union[int, fields.IntField] = fields.IntField(default=0)
    draw_sorted_numbers: Union[list, fields.JSONField] = fields.JSONField(null=True)

    user: User = fields.ForeignKeyField("models.User", related_name="Lottery")

    class Meta:
        table = "lottery"

    # TODO: Arrumar o timetools quando chegar na parte.

    def closed_a_time(self, ctx: Context):
        return ctx.translations.SupportTools.Humanize().Humanize.precisedelta(datetime.now(pytz.utc) - self.closed_in)


    def closed_in_str(self, ctx: Context):
        return ctx.translations.SupportTools.Humanize().Humanize.precisedelta(datetime.now(pytz.utc) - self.closed_in)
