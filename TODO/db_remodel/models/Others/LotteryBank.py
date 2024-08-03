from __future__ import annotations

from datetime import datetime
from tortoise import fields

from models.base import Base, TimestampMixin
from models.timezonefield import DatetimeTzField
import pytz
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from bot.bot import Context



class LotteryBank(Base, TimestampMixin):
    quantity = fields.IntField(default=0)
    closed_in = DatetimeTzField(null=True)
    closed = fields.BooleanField(default=False)
    accumulated = fields.BooleanField(default=True)
    drawn_numbers = fields.JSONField(null=True)
    accumulated_quantity = fields.IntField(default=0)

    class Meta:
        table = "loterica_banco"


    def encerrada_a_time(self, ctx: Context):
        return ctx.bot.TimeTools.Humanize.precisedelta(datetime.now(pytz.utc) - self.closed_in)


    def encerrada_em_(self):
        return self.closed_in.strftime("%d/%m/%Y %H:%M:%S")

    async def adicionar_aposta(self, valor):
        self.quantity += valor
        await self.save()
