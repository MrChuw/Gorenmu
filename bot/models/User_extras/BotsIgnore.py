from __future__ import annotations

from typing import TYPE_CHECKING

from tortoise import fields

from bot.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from bot.models.User import User


class BotsIgnore(Base, TimestampMixin):
    active: fields.BooleanField = fields.BooleanField(default=True)
    user: User = fields.ForeignKeyField("models.User", related_name="user_bot")

    user_id: int

    class Meta:
        unique_together = ("id", "user")
        table = "bots_ids"
