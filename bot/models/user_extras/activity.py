from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from tortoise import fields

if TYPE_CHECKING:
    from bot.ext import Context
    from bot.models import User

from bot.ext.named_tuples import RAfkNamedTuple
from bot.models.base import Base, TimestampMixin


class Status(Base, TimestampMixin):
    online: fields.BooleanField = fields.BooleanField(default=True)
    alias: fields.TextField = fields.TextField(null=True)
    message: fields.TextField = fields.TextField(null=True)
    updated_at: fields.DatetimeField = fields.DatetimeField(null=True)
    user: User = fields.ForeignKeyField("models.User", related_name="status")

    class Meta:
        table = "status"

    async def _go_afk(self, status, content):
        self.online = False
        self.alias = status.name
        self.message = content
        self.updated_at = datetime.datetime.now(datetime.UTC)
        await self.save()

    async def _go_rafk(self, status: RAfkNamedTuple):
        self.online = False
        self.alias = status.alias
        self.message = status.content
        self.updated_at = status.updated_at
        await self.save()

    @staticmethod
    async def get_afk(ctx: Context = None, user: User = None) -> Status:
        user = user or ctx.user
        status = await ctx.bot.memcache.Afk.get(user_id=user.id)
        if not status:
            response = await Status.get_or_create(user=user)
            status_db = response[0]
            await ctx.bot.memcache.Afk.set(user=user, value=status_db)
            status = status_db

        return status

    @staticmethod
    async def go_afk(ctx: Context, status, content):
        status_db = await Status.get_afk(ctx)
        await status_db._go_afk(status=status, content=content)

    @staticmethod
    async def go_rafk(ctx: Context, status: RAfkNamedTuple):  # NOQA
        await status.afk._go_rafk(status=status)
