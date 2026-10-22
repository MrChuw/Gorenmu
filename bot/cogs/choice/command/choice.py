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
        self.translations: Translations = Translations(bot, self)


    @commands.command(name="choice", aliases=["pick"])
    async def choice(self, ctx: Context, *, content: str) -> Response:  # NOQA
        pattern = self.translations.Choice.pattern(ctx.user.language)
        choice = random.choice([arg for arg in re.split(pattern, content) if arg])
        return self.translations.Choice.response(choice)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(ChoiceCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
