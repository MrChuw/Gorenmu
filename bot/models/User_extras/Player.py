from __future__ import annotations

from typing import TYPE_CHECKING

from tortoise import fields

from bot.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from bot.models.User import User


class Player(Base, TimestampMixin):
    class_ = fields.CharField(max_length=10)
    gender = fields.CharField(max_length=10)
    dungeon = fields.CharField(max_length=500)
    wins = fields.IntField(default=0)
    defeats = fields.IntField(default=0)
    level = fields.IntField(default=1)
    xp = fields.IntField(default=0)
    sub_class = fields.CharField(max_length=10, default="")

    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", related_name="player")

    class Meta:
        table = "player"

    def __str__(self) -> str:
        return f"{self.user.name} is a {self.class_}"
