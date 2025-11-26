from __future__ import annotations

from typing import TYPE_CHECKING

from tortoise import fields

from bot.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from bot.models.user import User


class Bug(Base, TimestampMixin):
    content: str | fields.TextField = fields.TextField()

    viewed: fields.BooleanField = fields.BooleanField(default=False)
    response: fields.TextField = fields.TextField(default=None, null=True)
    reminded: fields.BooleanField = fields.BooleanField(default=False)

    user: User = fields.ForeignKeyField("models.User", related_name="bug")

    class Meta:
        table = "bug"
