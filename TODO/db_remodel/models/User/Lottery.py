from __future__ import annotations

from datetime import datetime

import pytz
from tortoise import fields


from models.base import Base, TimestampMixin
from models.timezonefield import DatetimeTzField


from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from bot.bot import Context
    from models.User.User import User

class Loterica(Base, TimestampMixin):
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="Loterica"
    )
    apostado = fields.IntField(default=0)
    numeros = fields.JSONField(null=True)
    encerrada = fields.BooleanField(default=False)
    quantidade_ganha = fields.IntField(default=0, null=True)
    encerrada_em = DatetimeTzField(null=True)
    # acumulado = fields.BooleanField(default=False)
    numero_do_sorteio = fields.IntField(default=0)
    numeros_sorteados = fields.JSONField(null=True)

    class Meta:
        table = "loterica"


    def encerrada_a_time(self, ctx: Context):
        return ctx.bot.TimeTools.Humanize.precisedelta(datetime.now(pytz.utc) - self.encerrada_em)


    def encerrada_em_(self, ctx: Context):
        return ctx.bot.TimeTools.Humanize.precisedelta(datetime.now(pytz.utc) - self.encerrada_em)
