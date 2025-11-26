from __future__ import annotations

import asyncio
import random
from datetime import datetime
from typing import TYPE_CHECKING

import pytz
from tortoise import fields

from bot.models.base import Base

if TYPE_CHECKING:
    from bot.models.channel import Channel
    from bot.models.user import User


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

    def created_a_time(self, humanize, timezone):
        return humanize.precisedelta(datetime.now(timezone) - self.created_at.astimezone(timezone))

    @staticmethod
    async def all_messages_generator(maximum=None, category=None, offset=0, channel_id=None):
        batch_size = 100
        while not (maximum and offset >= maximum):
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
                users = await MessagesLog.filter(type=category).offset(offset).limit(batch_size).values("content")
            else:
                users = await MessagesLog.all().offset(offset).limit(batch_size)
            if not users:
                break
            await asyncio.sleep(0)
            all_users.extend(users)

            offset += batch_size
        return all_users

    @staticmethod
    async def get_random_message(user=None, channel=None):
        query = MessagesLog.filter()
        if user:
            query = query.filter(user=user)
        if channel:
            query = query.filter(channel=channel)

        min_id = await query.order_by("id").limit(1).values_list("id", flat=True)
        max_id = await query.order_by("-id").limit(1).values_list("id", flat=True)

        if not min_id or not max_id:
            return None, 0

        start_time = asyncio.get_event_loop().time()
        timeout = 30

        while asyncio.get_event_loop().time() - start_time < timeout:
            random_id = random.randint(min_id[0], max_id[0])
            message = await query.filter(id=random_id).prefetch_related("user").first()
            if message:
                return message, True

        return None, False
