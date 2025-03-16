from __future__ import annotations

import datetime
from tortoise import fields

from typing import Any, List, Optional, Tuple, TYPE_CHECKING, Union
if TYPE_CHECKING:
    from bot.models import User
    from bot.ext import Context

from bot.models.base import Base, TimestampMixin, TextFieldStr


class Status(Base, TimestampMixin):
    online: Union[bool, fields.BooleanField] = fields.BooleanField(default=True)
    alias: Union[str, fields.TextField] = fields.TextField(null=True)
    message: Union[str, fields.TextField] = fields.TextField(null=True)
    updated_at: Union[datetime, fields.DatetimeField] = fields.DatetimeField(null=True)
    user: User = fields.ForeignKeyField("models.User", related_name="status")

    class Meta:
        table = "status"

    async def _go_afk(self, status, content):
        self.online = False
        self.alias = status.name
        self.message = content
        self.updated_at = datetime.datetime.now(datetime.UTC)
        await self.save()

    async def _go_rafk(self, status):
        self.online = False
        self.alias = status["alias"]
        self.message = status["content"]
        self.updated_at = datetime.datetime.fromisoformat(status["updated_at"])
        await self.save()

    @staticmethod
    async def get_afk(ctx: Context = None, user: User = None, namespace: str = None):
        user_id = int(ctx.author.id) if ctx else user.id
        namespace = "afk" if namespace is None else namespace
        status = await ctx.bot.cache.get(key=user_id, namespace=namespace)
        if not status:
            status_db = (await Status.get_or_create(user=ctx.user))[0]
            if namespace == "afk" and not status:
                await ctx.bot.cache.set(key=user_id, value=status_db, namespace="afk")
            status = status_db

        return status

    @staticmethod
    async def go_afk(ctx: Context, status, content):
        status_db = await Status.get_afk(ctx)
        await status_db._go_afk(status=status, content=content)

    @staticmethod
    async def go_rafk(ctx: Context, status: dict):
        status_db = await Status.get_afk(ctx)
        await status_db._go_rafk(status=status)
















