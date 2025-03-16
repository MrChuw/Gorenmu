from __future__ import annotations

from datetime import datetime, UTC
from typing import Union

from bot.translations.extras import humanize as bot_humanize
from tortoise import fields, Model
import pytz


CharFieldStr = Union[str, fields.CharField]
IntFieldInt = Union[int, fields.IntField]
DatetimeTzField = Union[datetime, fields.DatetimeField]



class Base(Model):
    id: IntFieldInt = fields.IntField(pk=True)

    class Meta:
        abstract = True

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"


class TimestampMixin:
    created_at: DatetimeTzField = fields.DatetimeField(auto_now_add=True)
    updated_at: DatetimeTzField = fields.DatetimeField(auto_now=True)

    @property
    def created_ago(self):
        return datetime.now(pytz.utc) - self.created_at

    @property
    def updated_ago(self):
        return datetime.now(pytz.utc) - self.updated_at


    def created_a_time(self, humanize: bot_humanize.Humanize, timezone=UTC):
        return humanize.precisedelta(datetime.now(timezone) - self.created_at.astimezone(timezone))

    def updated_a_time(self, humanize: bot_humanize.Humanize, timezone=UTC):
        return humanize.precisedelta(datetime.now(timezone) - self.updated_at.astimezone(timezone))

    @property
    def created_em(self):
        return self.created_at.strftime("%d/%m/%Y %H:%M:%S")

    @property
    def updated_em(self):
        return self.updated_at.strftime("%d/%m/%Y %H:%M:%S")


class UserMixin:
    id: IntFieldInt = fields.IntField(pk=True, description="Twitch ID")
    name: CharFieldStr = fields.CharField(unique=True, index=True, max_length=64, description="Twitch username")


class ContentMixin:
    content: CharFieldStr = fields.CharField(max_length=1200, null=True, description="Twitch message content")


CharFieldIntStr = Union[int, fields.CharField]
TextFieldStr = Union[str, fields.TextField]
BoolFieldBool = Union[bool, fields.BooleanField]
FloatFieldFloat = Union[float, fields.FloatField]
