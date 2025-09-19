# -*- coding: utf-8 -*-
from __future__ import annotations

import random
import re
from typing import TYPE_CHECKING

from bot.ext import Context, Response, commands

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class ChoiceCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot)

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: Context) -> bool:  # NOQA
        return True

    @commands.command(name="choice", aliases=["pick"])
    async def choice(self, ctx: Context, *, content: str) -> Response:
        pattern = self.translations.Choice.pattern(ctx)
        choice = random.choice([arg for arg in re.split(pattern, content) if arg])
        return self.translations.Choice.response(ctx, choice)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(ChoiceCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
