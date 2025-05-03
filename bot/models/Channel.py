# -*- coding: utf-8 -*-
from __future__ import annotations

import datetime
from datetime import datetime
from typing import TYPE_CHECKING

from tortoise import fields
from tortoise.models import Model

from bot.models.base import CharFieldStr

if TYPE_CHECKING:
    from bot.models import MessagesLog, MarkovUsers, MarkovChannels  # NOQA


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
        return datetime.now(datetime.UTC) - self.created_at

    @property
    def updated_ago(self):
        return datetime.now(datetime.UTC) - self.updated_at


class Channel(Base, TimestampMixin):
    user = fields.ForeignKeyField("models.User", unique=True)
    followers = fields.IntField(null=True, description="Twitch followers")
    banwords = fields.JSONField(default={})
    disabled: dict[str, str] = fields.JSONField(
        default={
            "booru": "booru",
            "gelbooru": "gelbooru",
            "danbooru": "danbooru",
            "rule34": "rule34",
            "realbooru": "realbooru",
            "tbib": "tbib",
            "xbooru": "xbooru",
            "yandere": "yandere",
            "lolibooru": "lolibooru",
            "kanachan": "kanachan",
            "kanachan_net": "kanachan_net",
            "hypnohub": "hypnohub",
            "e621": "e621",
            "e926": "e926",
            "derpibooru": "derpibooru",
            "furbooru": "furbooru",
            "atfbooru": "atfbooru",
            "behoimi": "behoimi",
            "paheal": "paheal",
        }
    )
    online = fields.BooleanField(default=True)
    prefix = fields.CharField(max_length=2, default="+")
    removed = fields.BooleanField(default=False)
    language: CharFieldStr = fields.CharField(max_length=32, null=True)

    messages = fields.ReverseRelation["MessagesLog"]

    markov = fields.ReverseRelation["MarkovUsers"]
    markov_channels = fields.ReverseRelation["MarkovChannels"]

    class Meta:
        table = "channel"
