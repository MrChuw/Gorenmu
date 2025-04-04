from __future__ import annotations

from typing import TYPE_CHECKING

from tortoise import fields, Model

from bot.models.base import TimestampMixin

if TYPE_CHECKING:
    from bot.models.User import User


class MarkovChannels(Model, TimestampMixin):
    curr_state = fields.CharField(max_length=255)
    transition = fields.JSONField()

    channel: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
            "models.Channel", related_name="MarkovChannels"
    )

    class Meta:
        unique_together = ("curr_state", "channel")
        table = "markov_channels"
