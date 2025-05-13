# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import commands, Context
from bot.models import Status
from bot.translations import afks, BaseDecorators, Response
from bot.ext.named_tuples import RAfkNamedTuple

if TYPE_CHECKING:
    from bot.bot import Gorenmu

rafk_alias = [f"r{s}" for s in afks.afks if s != "afk"]


class RAfkCmd(commands.CustomComponent):
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

    @commands.base_decorator(BaseDecorators.RAfk)
    @commands.command(name='rafk', aliases=rafk_alias)
    async def rafk(self, ctx: Context, *, content: str = "") -> Response:
        translations = ctx.user.translations
        rafk = await self.bot.memcache.RAfk.get(user_id=ctx.author.id)
        if rafk is None:
            return translations.Exceptions.time_expired.format_response(ctx, ctx.user.translations.RAfk.return_expired, success=False, pipe=False)

        status = ctx.user.translations.Afk.afks[rafk.alias]
        await Status.go_rafk(ctx, rafk)
        if rafk.content == "":
            return translations.RAfk.is_afk.format_response(ctx, status.leave_again, status.emoji, pipe=False)
        else:
            return translations.RAfk.is_afk_content.format_response(
                    ctx,
                    status.leave_again,
                    status.emoji,
                    rafk.content,
                    pipe=False
            )



async def setup(bot: Gorenmu) -> None:
    await bot.add_component(RAfkCmd(bot))


async def teardown(bot: Gorenmu) -> None:
    ...
