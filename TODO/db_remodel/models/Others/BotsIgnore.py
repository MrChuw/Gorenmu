from __future__ import annotations

from tortoise import fields

from models.base import Base, TimestampMixin
from models.User.User import User


class Bots_ignore(Base, TimestampMixin):
    ativo = fields.BooleanField(default=True)

    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="user_bot"
    )

    class Meta:
        unique_together = ("id", "user")
        table = "bots_ids"
