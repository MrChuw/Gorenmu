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

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    async def component_before_invoke(self, ctx: Context) -> None:
        self.translations.ctx_set(ctx)

    @commands.Component.guard()
    def guards_component(self, ctx: Context) -> bool:  # NOQA
        return True

    @commands.command(name="upsidedown", aliases=["updown"])
    async def upsidedown(self, ctx: Context, *, content) -> Response:
        return self.translations.UpSideDown.upsidedown(transform(content))


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(UpSideDownCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
