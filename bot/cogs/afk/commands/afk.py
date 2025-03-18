# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import TYPE_CHECKING

from bot.ext import commands, Context
from bot.translations import BaseDecorators, Response, afks
from bot.utils import Role
from bot.models import Status

if TYPE_CHECKING:
    from bot.bot import Gorenmu

__all__ = (
        'AFKCmd'
)

BaseDeco = BaseDecorators.Afk
afk_alias = [s for s in afks.afks if s != "afk"]


class AFKCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None:
        ...

    @commands.Component.guard()
    def guards_component(self, ctx: commands.Context) -> bool:
        return True

    @commands.base_decorator(BaseDeco)
    @commands.command(name='afk', aliases=afk_alias)
    async def afk(self, ctx: Context, *, content: str = "", ) -> Response:
        translations = ctx.user.translations.Afk
        if len(content) >= 450:
            return translations.message_too_long.format_response(ctx, success=False, pipe=False)
        afk = translations.afks.get(ctx.invoke_by)  # NOQA
        await Status.go_afk(ctx=ctx, status=afk, content=content)
        if not content:
            return translations.afk_response.format_response(ctx, afk.leave, afk.emoji, pipe=False)
        else:
            return translations.afk_content_response.format_response(ctx, afk.leave, afk.emoji, content, pipe=False)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(AFKCmd(bot))


async def teardown(bot: Gorenmu) -> None:
    ...
