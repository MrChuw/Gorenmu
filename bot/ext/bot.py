from __future__ import annotations

import asyncio
import datetime
from asyncio import Task
from collections import defaultdict
from collections.abc import Callable
from typing import TYPE_CHECKING

from twitchio.ext import commands
from twitchio.user import User

if TYPE_CHECKING:
    from bot.ext import commands
    from bot.ext.commands import Command, Group
    from bot.models import Channel as ChannelModel
    from bot.utils import MarkovProcessor, SemaphoreManager


class TypesBot(commands.AutoBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.MarkovProcessor: MarkovProcessor | None = None
        self.MarkovTask: Task[None] | None = None
        self.dev_user: User | None = None
        self.bot_user: User | None = None
        self.mock: bool = kwargs.get("mock", False)
        self.lottery_lock: asyncio.Lock = asyncio.Lock()
        self.channels: dict[str, ChannelModel] = {}
        self.bots_ids: list[int] = []
        self.boot: datetime.datetime = datetime.datetime.now(datetime.UTC)
        self.manual_events: defaultdict[str, dict[str, dict[str, Callable]]] = defaultdict(lambda: defaultdict(dict))
        self.disable_default: list[str] = []
        self.SemaphoreManager: SemaphoreManager | None = None

    def get_command(self, name: str, /) -> Command | Group | None:
        return super().get_command(name)
