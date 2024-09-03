from __future__ import annotations

from datetime import datetime

from typing import Any, List, Optional, Tuple, TYPE_CHECKING, Union
from tortoise.models import Model
from tortoise import fields
from twitchio.ext.commands import Command

from bot.models.base import TimestampMixin
import json

if TYPE_CHECKING:
    from bot.models.User import User
    from bot.models.Channel import Channel
    from bot.ext import Context


class Alias(Model, TimestampMixin):
    id = fields.IntField(pk=True, index=True)
    user: User = fields.ForeignKeyField("models.User", related_name="Alias", null=True, on_delete=fields.SET_NULL)
    channel: Channel = fields.ForeignKeyField("models.Channel", related_name="Alias", null=True, on_delete=fields.SET_NULL)
    name = fields.CharField(max_length=50, index=True)
    command = fields.CharField(max_length=50, null=True)
    invocation = fields.CharField(max_length=50, null=True)
    arguments = fields.JSONField(null=True)
    description = fields.TextField(null=True)
    parent = fields.ForeignKeyField('models.Alias', related_name='children', null=True, on_delete=fields.SET_NULL)
    deleted = fields.BooleanField(default=False)

    class Meta:
        table = 'command_alias'
        verbose_name = 'Custom Command Alias'
        verbose_name_plural = 'Custom Command Aliases'
    indexes = [("user", "channel", "name"), ("channel",), ("command",), ("parent",)]

    @staticmethod
    async def save_alias(ctx: Context, name: str,
                         command_check: Command, command_, rest) -> Alias:
        alias = Alias(
                user_id=ctx.author.id,
                channel_id=None,
                name=name,
                command=command_check.name,
                invocation=command_,
                arguments=rest if rest else None)
        await alias.save()
        return alias




    @staticmethod
    async def link_alias(user: User, name: str, parent: Alias):
        alias = Alias(user=user, name=name, description=parent.description, parent=parent)
        await alias.save()
        return alias





















