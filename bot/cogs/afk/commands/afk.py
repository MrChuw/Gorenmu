# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import commands, Context
from bot.models import Status
from bot.translations import afks, Response

if TYPE_CHECKING:
    from bot.bot import Gorenmu

afk_alias = [s for s in afks.afks if s != "afk"]


class AFKCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: Context) -> bool:  # NOQA
        return True

    @commands.base_decorator("Afk")
    @commands.command(name="afk", aliases=afk_alias)
    async def afk(self, ctx: Context, *, content: str = "") -> Response:
        translations = ctx.user.translations
        if len(content) >= 450:
            return translations.Exceptions.too_much_characters.format_response(ctx, success=False)
        afk = translations.Afk.afks.get(ctx.invoke_by)  # NOQA
        await Status.go_afk(ctx=ctx, status=afk, content=content)
        if not content:
            return translations.Afk.afk_response.format_response(ctx, afk.leave, afk.emoji)
        return translations.Afk.afk_content_response.format_response(ctx, afk.leave, afk.emoji, content)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(AFKCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
