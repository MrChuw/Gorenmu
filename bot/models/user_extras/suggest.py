from __future__ import annotations

from typing import TYPE_CHECKING

from tortoise import fields

from bot.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from bot.models.user import User


class Suggest(Base, TimestampMixin):
    content = fields.TextField()

    viewed = fields.BooleanField(default=False)
    response = fields.TextField(default=None, null=True)
    reminded = fields.BooleanField(default=False)

    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", related_name="suggest")

    class Meta:
        table = "suggest"
