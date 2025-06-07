from __future__ import annotations

from typing import TYPE_CHECKING

from tortoise import fields, Model

from bot.models.base import TimestampMixin

if TYPE_CHECKING:
    from bot.models.User import User


class MarkovUsers(Model, TimestampMixin):
    curr_state = fields.CharField(max_length=255)
    transition = fields.JSONField()
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", related_name="MarkovUsers")

    class Meta:
        unique_together = ("curr_state", "user")
        table = "markov_users"
