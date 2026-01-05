from __future__ import annotations

from typing import TYPE_CHECKING

from bot.models import Channel as ChannelModel

if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.ext import ChatMessage


class ChannelHandler:
    def __init__(self, bot: Gorenmu):
        self.bot = bot

    async def load_channels(self) -> None:
        for channel in await ChannelModel.filter(removed=False):
            self.bot.channels[(await channel.user).name.lower()] = channel
        ...

    async def is_online(self, message: ChatMessage) -> bool:
        return (
            message.text.startswith(f"{self.bot.channels[message.broadcaster.name].prefix}start")
            or self.bot.channels[message.broadcaster.name].online
        )

    async def setup(self): ...

    async def teardown(self) -> None: ...
