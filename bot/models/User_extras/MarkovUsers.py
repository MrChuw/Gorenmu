from __future__ import annotations

from tortoise import Model, fields

from models.base import TimestampMixin
from models.User.User import User


class MarkovUsers(Model, TimestampMixin):
    curr_state = fields.CharField(max_length=255)
    transition = fields.JSONField()
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="MarkovUsers"
    )

    class Meta:
        unique_together = ("curr_state", "user")
        table = "markov_users"
