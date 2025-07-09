# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import commands, Context
from bot.translations import Response

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class SafeBooruCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: Context) -> bool:  # NOQA
        return True

    @commands.base_decorator("Safebooru")
    @commands.command(name="safebooru", aliases=[])
    async def safebooru(self, ctx: Context, *, args) -> Response:
        translations = ctx.user.translations.Admin.Nada
        return translations.nada.format_response(ctx, args, success=True, handle=None, response_list=[])


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(SafeBooruCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
