from __future__ import annotations

from typing import TYPE_CHECKING

from tortoise import fields

from bot.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from bot.models.User import User


class Copypasta(Base, TimestampMixin):
    content: fields.TextField = fields.TextField()
    visible: fields.BooleanField = fields.BooleanField(default=True)

    user: User = fields.ForeignKeyField("models.User", related_name="Copypasta")

    class Meta:
        table = "copypasta"
