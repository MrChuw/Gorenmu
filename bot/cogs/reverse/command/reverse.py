from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Context, Response, commands

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class ReverseCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot, self)

    @commands.command(name="reverse", aliases=["invert"])
    async def reverse(self, ctx: Context, *, content: str) -> Response:  # NOQA
        return self.translations.Exceptions.echo(content[::-1])


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(ReverseCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
