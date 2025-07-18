# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from twitchio.ext import commands

if TYPE_CHECKING:
    from .commands import Command


class TypesBot(commands.AutoBot):
    def get_command(self, name: str, /) -> Optional[Command]:
        return super().get_command(name)
