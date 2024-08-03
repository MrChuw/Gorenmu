from __future__ import annotations

import asyncio
import random
from datetime import datetime

import pytz
from tortoise import fields
from urlextract import URLExtract

from models.base import Base
from models.timezonefield import DatetimeTzField
from typing import Any, List, Optional, Tuple, TYPE_CHECKING, Union


if TYPE_CHECKING:
    from bot.bot import Context
    from models.User.User import User

class Mensage_log(Base):
    content = fields.TextField()
    created_at = DatetimeTzField(auto_now_add=True)
    type = fields.TextField()

    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="messages"
    )
    channel: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.Channel", related_name="messages", null=True
    )

    class Meta:
        table = "mensage_logs"

    @property
    def created_ago(self):
        return datetime.now(pytz.utc) - self.created_at


    def created_a_time(self, ctx: Context):
        return ctx.bot.TimeTools.Humanize.precisedelta(datetime.now(pytz.utc) - self.created_at)

    async def all_mensagens_generator(maximo=None, filtro=None, offset=0, canal_id=None):
        # batch_size = 100
        # while True:
        # 	if maximo and offset >= maximo:
        # 		break
        # 	if filtro == "message":
        # 		users = await Mensage_log.filter(type=filtro).offset(offset).limit(batch_size).values('content')
        # 	else:
        # 		users = await Mensage_log.all().offset(offset).limit(batch_size)
        # 	if not users:
        # 		break
        # 	for user in users:
        # 		yield user
        # 	offset += batch_size

        batch_size = 100
        while True:
            if maximo and offset >= maximo:
                break
            cursor = Mensage_log.all()

            if filtro == "message":
                cursor = cursor.filter(type=filtro)

            if canal_id:
                cursor = cursor.filter(channel_id=canal_id)

            users = await cursor.offset(offset).limit(batch_size)
            if not users:
                break
            for user in users:
                yield user
            offset += batch_size

    async def all_mensagens(maximo=None, filtro=None):
        batch_size = 100
        offset = 0
        users_fetched = True
        all_users = []

        while users_fetched and (not maximo or len(all_users) < maximo):
            if filtro == "message":
                users = (
                    await Mensage_log.filter(type=filtro)
                    .offset(offset)
                    .limit(batch_size)
                    .values("content")
                )
            else:
                users = await Mensage_log.all().offset(offset).limit(batch_size)
            if not users:
                users_fetched = False
                break
            await asyncio.sleep(0)
            all_users.extend(users)

            offset += batch_size
        return all_users

    async def random_line(ctx: Context, tipo, alvo=None):
        if tipo == "canal":
            if alvo:
                channel = ctx.bot.channels[alvo]
            else:
                channel = ctx.bot.channels[ctx.channel.name]
            count_value = await Mensage_log.filter(channel=channel).count()
            random_offset = random.randint(0, count_value - 1)
            random_ = (
                await Mensage_log.filter(channel=channel).offset(random_offset).limit(1).first()
            )
        elif tipo == "global":
            count_value = await Mensage_log.all().count()
            random_offset = random.randint(0, count_value - 1)
            random_ = await Mensage_log.all().offset(random_offset).limit(1).first()
        elif tipo == "usuario":
            user = await User.get(name=alvo) if alvo else ctx.user
            count_value = await Mensage_log.filter(
                channel=ctx.bot.channels[ctx.channel.name], user=user
            ).count()
            random_offset = random.randint(0, count_value - 1)
            random_ = await Mensage_log.filter(user=user).offset(random_offset).limit(1).first()
        return random_
