from __future__ import annotations

from typing import TYPE_CHECKING, Any

from bot.ext import ChatMessage, Context
from bot.models import Channel as ChannelModel

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class ChannelHandler:
    def __init__(self, bot: Gorenmu):
        self.bot = bot
        if not self.bot.channels:
            self.bot.channels = ChannelManager()

    async def load_channels(self) -> None:
        for channel in await ChannelModel.filter(removed=False):
            self.bot.channels[(await channel.user).name.lower()] = channel

    async def is_online(self, target: Context | ChatMessage) -> bool:
        message = target.message.text if isinstance(target, Context) else target.text
        start = f"{self.bot.channels.prefix(target)}start"

        return message.startswith(start) or self.bot.channels.is_online(target)

    async def is_enabled(self, target: Context | ChatMessage, command_name: str = "") -> bool:
        return await self.bot.CommandHandler.is_enabled(target, command=command_name)

    async def setup(self):
        if not self.bot.channels:
            self.bot.channels = ChannelManager()

    async def teardown(self) -> None: ...


class ChannelManager:
    def __init__(self):
        self._channels: dict[str, ChannelModel] = {}

    def __setitem__(self, key: str, value: ChannelModel) -> None:
        self._channels[key.lower()] = value

    def __getitem__(self, key: str | None) -> ChannelModel | None:
        if not key:  # sourcery skip: assign-if-exp, reintroduce-else
            return None
        return self._channels.get(key.lower(), None)

    def __contains__(self, key: object) -> bool:
        if not isinstance(key, str):  # sourcery skip: assign-if-exp
            return False
        return self._channels.__contains__(key.lower())

    def __len__(self) -> int:
        return len(self._channels)

    def _get_name(self, target: Any) -> str | None:
        if isinstance(target, str):
            return target

        if hasattr(target, "channel") and hasattr(target.channel, "name"):
            return target.channel.name

        if hasattr(target, "broadcaster") and hasattr(target.broadcaster, "name"):
            return target.broadcaster.name

        if hasattr(target, "name"):  # sourcery skip: assign-if-exp, reintroduce-else
            return target.name

        return None

    def get_channel(self, target: Context | ChatMessage) -> ChannelModel | None:
        name = self._get_name(target)
        if not name:  # sourcery skip: assign-if-exp, reintroduce-else
            return None
        return self._channels.get(name.lower())

    def get_channel_by_name(self, name: str) -> ChannelModel | None:
        return self._channels.get(name.lower())

    def is_online(self, target: Context | ChatMessage) -> bool:
        channel = self.get_channel(target)
        return channel.online if channel else False

    def prefix(self, target: Context | ChatMessage) -> str | None:
        channel = self.get_channel(target)
        return channel.prefix if channel else "+"

    def banwords(self, target: Context | ChatMessage) -> dict:
        channel = self.get_channel(target)
        return channel.banwords if channel else {}

    def disabled(self, target: Context | ChatMessage) -> dict:
        channel = self.get_channel(target)
        return channel.disabled if channel else {}

    def all(self) -> dict[str, ChannelModel]:
        return self._channels
