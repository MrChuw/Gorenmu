from __future__ import annotations

from typing import TYPE_CHECKING

from tortoise import fields

from bot.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from bot.models.user import User


class PlayerTower(Base, TimestampMixin):
    class_ = fields.CharField(max_length=10)
    sub_class = fields.CharField(max_length=10, default="")
    gender = fields.CharField(max_length=10)
    encontro = fields.TextField(null=True)
    quote = fields.JSONField(null=True)
    choice = fields.CharField(max_length=500, null=True)
    wins = fields.IntField(default=0)
    defeats = fields.IntField(default=0)
    level = fields.IntField(default=1)
    andar = fields.IntField(default=1)
    zona = fields.IntField(default=1)
    xp = fields.IntField(default=0)
    cooldown = fields.IntField(default=0)

    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", related_name="player_torre")

    class Meta:
        table = "player_tower"
