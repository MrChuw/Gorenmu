# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from tortoise import Tortoise
from tortoise.exceptions import DoesNotExist

from bot.models import Channel as ChannelModel, User as UserModel

if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.utils import Config


class DatabaseHandler:
    def __init__(self, bot: Gorenmu):
        self.bot = bot
        self.config: Config = bot.config

    async def setup_database(self) -> None:
        await Tortoise.init(config=self.config.DatabaseConfig.DB_CONFIG)
        # await migrations()
        await Tortoise.generate_schemas()
        try:
            user = await UserModel.get(id=411010313)
        except DoesNotExist:
            user = await UserModel.create_or_none(411010313, "MrChuw")
        try:
            await ChannelModel.get(user=user)
        except DoesNotExist:
            await ChannelModel.create(user=user)

    @staticmethod
    async def close_db() -> None:
        await Tortoise.close_connections()
