# -*- coding: utf-8 -*-
from __future__ import annotations

import random
from typing import TYPE_CHECKING

from bot.ext import Context, commands
from bot.translations import Response

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class ChanceCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: Context) -> bool:  # NOQA
        return True

    @commands.base_decorator("Chance")
    @commands.command(name="chance", aliases=["%"])
    async def chance(self, ctx: Context) -> Response:
        chance = f'{("{:.2f}%".format(random.random() * 100))}'
        return ctx.user.translations.Chance.random_percentage.format_response(ctx, chance)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(ChanceCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
