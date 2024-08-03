from __future__ import annotations

import asyncio
import random
from datetime import datetime

import pytz
from tortoise import fields

from bot.models.base import Base, TimestampMixin
from typing import Any, List, Optional, Tuple, TYPE_CHECKING, Union


if TYPE_CHECKING:
    from bot.bot import Context
    from bot.models.User import User
    from bot.models.Channel import Channel


class MessagesLog(Base):
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    type = fields.TextField()

    user: User = fields.ForeignKeyField("models.User", related_name="MessagesLog")
    channel: Channel = fields.ForeignKeyField("models.Channel", related_name="MessagesLog", null=True)

    class Meta:
        table = "message_logs"

    @property
    def created_ago(self):
        return datetime.now(pytz.utc) - self.created_at


    def created_a_time(self, ctx: Context):
        return ctx.translations.SupportTools.Humanize().Humanize.precisedelta(datetime.now(pytz.utc) - self.created_at)

    @staticmethod
    async def all_messages_generator(maximum=None, category=None, offset=0, channel_id=None):
        batch_size = 100
        while True:
            if maximum and offset >= maximum:
                break
            cursor = MessagesLog.all()

            if category == "message":
                cursor = cursor.filter(type=category)

            if channel_id:
                cursor = cursor.filter(channel_id=channel_id)

            users = await cursor.offset(offset).limit(batch_size)
            if not users:
                break
            for user in users:
                yield user
            offset += batch_size

    @staticmethod
    async def all_messages(maximum=None, category=None):
        batch_size = 100
        offset = 0
        users_fetched = True
        all_users = []

        while users_fetched and (not maximum or len(all_users) < maximum):
            if category == "message":
                users = (
                    await MessagesLog.filter(type=category)
                    .offset(offset)
                    .limit(batch_size)
                    .values("content")
                )
            else:
                users = await MessagesLog.all().offset(offset).limit(batch_size)
            if not users:
                users_fetched = False
                break
            await asyncio.sleep(0)
            all_users.extend(users)

            offset += batch_size
        return all_users

    @staticmethod
    async def random_line(ctx: Context, category, target=None):
        line = None
        if category == "channel":
            if target:
                channel = ctx.bot.channels[target]
            else:
                channel = ctx.bot.channels[ctx.channel.name]
            count_value = await MessagesLog.filter(channel=channel).count()
            random_offset = random.randint(0, count_value - 1)
            line = (
                await MessagesLog.filter(channel=channel).offset(random_offset).limit(1).first()
            )
        elif category == "global":
            count_value = await MessagesLog.all().count()
            random_offset = random.randint(0, count_value - 1)
            line = await MessagesLog.all().offset(random_offset).limit(1).first()
        elif category == "user":
            user = await User.get(name=target) if target else ctx.user
            count_value = await MessagesLog.filter(
                channel=ctx.bot.channels[ctx.channel.name], user=user
            ).count()
            random_offset = random.randint(0, count_value - 1)
            line = await MessagesLog.filter(user=user).offset(random_offset).limit(1).first()
        return line
