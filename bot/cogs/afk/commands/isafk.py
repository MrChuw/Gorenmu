# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Context, commands
from bot.models import User
from bot.translations import Response

if TYPE_CHECKING:
    from bot.bot import Gorenmu

from bot.models import Status


class IsAfkCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: Context) -> bool:  # NOQA
        return True

    @commands.base_decorator("IsAfk")
    @commands.command(name="isafk", aliases=[])
    async def isafk(self, ctx: Context, *, content: str) -> Response:
        translations = ctx.user.translations
        name = ctx.bot.StringTools.str2name(content.split()[0])
        actions = {
            ctx.bot.bot_nick: translations.IsAfk.bot_nick.format_response(ctx, success=False),
            ctx.author.name: translations.IsAfk.author_nick.format_response(ctx, success=False),
        }
        if name in actions:
            return actions[name]
        user = await User.get_user(ctx=ctx, name=name, is_none=True) if name != ctx.author.name.lower() else ctx.user
        if not user:
            return translations.Exceptions.never_seen.format_response(ctx, name)
        afk = await Status.get_afk(ctx=ctx, user=user)
        if afk.online:
            return translations.IsAfk.is_not_afk.format_response(ctx, name)
        status = ctx.user.translations.Afk.afks[afk.alias]
        time = ctx.user.translations.SupportTools.TimeTools.Humanize.updated_a_time(afk.updated_at)
        if not afk.message:
            return translations.IsAfk.is_afk.format_response(ctx, name, status.current, status.emoji, time)
        return translations.IsAfk.is_afk_content.format_response(
            ctx, name, status.current, status.emoji, afk.message, time
        )


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(IsAfkCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
