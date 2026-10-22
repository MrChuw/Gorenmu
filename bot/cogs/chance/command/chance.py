from __future__ import annotations

import random
from typing import TYPE_CHECKING

from bot.ext import Context, Response, commands

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class ChanceCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot, self)

    @commands.Component.guard()
    def guards_component(self, ctx: Context) -> bool:  # NOQA
        return True

    @commands.command(name="chance", aliases=["%"])
    async def chance(self, ctx: Context) -> Response:  # NOQA
        chance = f"{random.random() * 100:.2f}%"
        return self.translations.Chance.response(chance)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(ChanceCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
