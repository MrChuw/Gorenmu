from __future__ import annotations

from tortoise import fields

from bot.models.base import Base, TimestampMixin
from typing import Any, List, Optional, Tuple, TYPE_CHECKING, Union
if TYPE_CHECKING:
    from bot.models.User import User


class Wedding(Base, TimestampMixin):
    user_1: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="user_1"
    )  # TODO: corrigir esse daqui tbm user_id_1
    user_2: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="user_2"
    )  # TODO: corrigir esse daqui tbm user_id_2
    casados = fields.BooleanField(default=True)
    quem_separou = fields.IntField(null=True)

    class Meta:
        table = "wedding"

    async def divorce(self, user_id: int):
        self.casados = False
        self.quem_separou = user_id
        await self.save()
