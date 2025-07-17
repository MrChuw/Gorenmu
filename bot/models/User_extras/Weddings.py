from __future__ import annotations

from typing import TYPE_CHECKING

from tortoise import fields

from bot.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from bot.models.User import User


class Wedding(Base, TimestampMixin):
    user_1: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", related_name="user_1")
    user_2: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", related_name="user_2")
    active_marriage = fields.BooleanField(default=True)
    who_separated = fields.IntField(null=True)

    class Meta:
        table = "wedding"

    async def divorce(self, user_id: int):
        self.active_marriage = False
        self.who_separated = user_id
        await self.save()
