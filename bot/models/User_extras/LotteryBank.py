from __future__ import annotations

from datetime import datetime
from tortoise import fields
from typing import Union

from bot.models.base import Base, TimestampMixin
import pytz
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from bot.bot import Context



class LotteryBank(Base, TimestampMixin):
    quantity: Union[int, fields.IntField] = fields.IntField(default=0)
    closed_in: Union[datetime, fields.DatetimeField] = fields.DatetimeField(null=True)
    closed: Union[bool, fields.BooleanField] = fields.BooleanField(default=False)
    accumulated: Union[bool, fields.BooleanField] = fields.BooleanField(default=True)
    drawn_numbers: Union[list, fields.JSONField] = fields.JSONField(null=True)
    accumulated_quantity: Union[int, fields.IntField] = fields.IntField(default=0)

    class Meta:
        table = "lottery_bank"

    # TODO: Arrumar o timetools quando chegar na parte. end_at

    def end_at(self, ctx: Context):
        return ctx.translations.SupportTools.Humanize().Humanize.precisedelta(datetime.now(pytz.utc) - self.closed_in)


    def end_at_strftime(self):
        return self.closed_in.strftime("%d/%m/%Y %H:%M:%S")

    async def add(self, value: int):
        self.quantity += value
        await self.save()