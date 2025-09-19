# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from twitchio.ext import commands

if TYPE_CHECKING:
    from bot.ext import commands
    from bot.ext.commands import Command, Group


class TypesBot(commands.AutoBot):
    def get_command(self, name: str, /) -> Optional[Command | Group]:
        return super().get_command(name)
