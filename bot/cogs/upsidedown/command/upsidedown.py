from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Context, Response, commands

from .extras import transform
from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class UpSideDownCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot, self)

    @commands.command(name="upsidedown", aliases=["updown"])
    async def upsidedown(self, ctx: Context, *, content) -> Response:  # noqa
        return self.translations.UpSideDown.upsidedown(transform(content))


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(UpSideDownCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
