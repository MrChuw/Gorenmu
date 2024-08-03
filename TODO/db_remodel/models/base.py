from __future__ import annotations

from datetime import datetime
from typing import Union

import humanize
from tortoise import fields, Model

from models.timezonefield import DatetimeTzField

CharFieldStr = Union[str, fields.CharField]
IntFieldInt = Union[int, fields.IntField]
DatetimeTzFieldDt = Union[datetime, DatetimeTzField]

import pytz



class Base(Model):
    id: IntFieldInt = fields.IntField(pk=True)

    class Meta:
        abstract = True

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"


class TimestampMixin:
    created_at: DatetimeTzFieldDt = DatetimeTzField(auto_now_add=True)
    updated_at: DatetimeTzFieldDt = DatetimeTzField(auto_now=True)

    @property
    def created_ago(self):
        return datetime.utcnow() - self.created_at

    @property
    def updated_ago(self):
        return datetime.utcnow() - self.updated_at

    @property
    def created_a_time(self):
        return humanize.precisedelta(datetime.now(pytz.utc) - self.created_at)

    @property
    def updated_a_time(self):
        return humanize.precisedelta(datetime.now(pytz.utc) - self.updated_at)

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
NickHistory = Union[list[str], fields.TextField]
