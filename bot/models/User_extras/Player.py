from __future__ import annotations

from tortoise import fields

from bot.models.base import Base, TimestampMixin, CharFieldStr, CharFieldIntStr, IntFieldInt
from typing import Any, List, Optional, Tuple, TYPE_CHECKING, Union
if TYPE_CHECKING:
    from bot.models.User import User


class Player(Base, TimestampMixin):
    class_: CharFieldStr = fields.CharField(max_length=10)
    gender: CharFieldStr = fields.CharField(max_length=10)
    dungeon: CharFieldIntStr = fields.CharField(max_length=500)
    wins: IntFieldInt = fields.IntField(default=0)
    defeats: IntFieldInt = fields.IntField(default=0)
    level: IntFieldInt = fields.IntField(default=1)
    xp: IntFieldInt = fields.IntField(default=0)
    sub_class: CharFieldStr = fields.CharField(max_length=10, default="")

    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="player"
    )

    class Meta:
        table = "player"

    def __str__(self) -> str:
        return f"{self.user.name} is a {self.class_}"
