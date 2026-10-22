from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from tortoise import fields
from tortoise.models import Model, Field

from bot.models.base import CharFieldStr

if TYPE_CHECKING:
    from bot.models import MarkovChannels, MarkovUsers, MessagesLog  # NOQA
    from bot.models import User


class Base(Model):
    id = fields.IntField(primary_key=True)

    class Meta:
        abstract = True

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"


class TimestampMixin:
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    @property
    def created_ago(self):
        return datetime.now(UTC) - self.created_at

    @property
    def updated_ago(self):
        return datetime.now(UTC) - self.updated_at


class Channel(Base, TimestampMixin):
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", unique=True)
    followers: fields.Field[int | None] = fields.IntField(null=True, description="Twitch followers")  # ty: ignore[invalid-assignment] # noqa: E501
    banwords: fields.Field[dict[str, int]] = fields.JSONField(default={})
    disabled: fields.Field[dict[str, int]] = fields.JSONField(default={})
    online: fields.Field[bool] = fields.BooleanField(default=True)
    prefix: fields.Field[str] = fields.CharField(max_length=2, default="+")
    removed: fields.Field[bool] = fields.BooleanField(default=False)
    language: fields.Field[str | None] = fields.CharField(max_length=32, null=True)  # ty: ignore[invalid-assignment]
    event_subs: fields.Field[dict[str, str]] = fields.JSONField(default={})

    messages = fields.ReverseRelation["MessagesLog"]
    markov = fields.ReverseRelation["MarkovUsers"]
    markov_channels = fields.ReverseRelation["MarkovChannels"]

    user_id: int

    class Meta:
        table = "channel"
