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

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    async def component_before_invoke(self, ctx: Context) -> None:
        self.translations.ctx_set(ctx)

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
