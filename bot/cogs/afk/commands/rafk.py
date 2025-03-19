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
        'RAfkCmd'
)

BaseDeco = BaseDecorators.RAfk
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

    @commands.base_decorator(BaseDeco)
    @commands.command(name='rafk', aliases=rafk_alias)
    async def rafk(self, ctx: Context, *, content, ) -> Response:
        translations = ctx.user.translations
        afk = await Status.get_afk(ctx, namespace="rafk")
        if afk is None:
            return translations.Exceptions.time_expired.format_response(ctx, success=False)
        elif afk["alias"] in ctx.user.translations.Afk.afks:
            status = ctx.user.translations.Afk.afks["alias"]
            await ctx.bot.memcache.delete(f"Afk-{ctx.author.id}")
            await Status.go_rafk(ctx, afk)
            if afk["content"] == "":
                return translations.RAfk.is_afk.format_response(ctx, status.leave_again, status.emoji, pipe=False)
            else:
                return translations.RAfk.is_afk.format_response(
                        ctx,
                        status.leave_again,
                        status.emoji, afk["content"],
                        pipe=False
                )
        else:
            return translations.RAfk.is_not_afk.format_response(ctx, success=False, pipe=False)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(RAfkCmd(bot))


async def teardown(bot: Gorenmu) -> None:
    ...
