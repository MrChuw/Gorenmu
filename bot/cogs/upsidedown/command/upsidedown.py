# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from bot.apis.upsidedown import transform
from bot.ext import commands, Context
from bot.translations import BaseDecorators, Response

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class UpSideDownCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: commands.Context) -> bool:  # NOQA
        return True

    @commands.base_decorator(BaseDecorators.UpSideDown)
    @commands.command(name="upsidedown", aliases=["updown"])
    async def upsidedown(self, ctx: Context, *, content) -> Response:
        return ctx.user.translations.UpSideDown.upsidedown.format_response(ctx, transform(content))


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(UpSideDownCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
