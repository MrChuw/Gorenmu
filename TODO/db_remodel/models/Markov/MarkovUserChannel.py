from __future__ import annotations

from tortoise import Model, fields

from models.base import TimestampMixin
from models.User.User import User


class MarkovUserChannel(Model, TimestampMixin):
    curr_state = fields.CharField(max_length=255)
    transition = fields.JSONField()

    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="markov_user_canal"
    )

    channel: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.Channel", related_name="markov_user_canal"
    )  # mais so ser único em relacao a este

    class Meta:
        unique_together = ("curr_state", "user", "channel")
        table = "markov_model_user_canal"
