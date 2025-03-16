# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import TYPE_CHECKING

from bot.ext import commands, Context
from bot.translations import BaseDecorators, Response
from bot.utils import Role
from bot.models import User

if TYPE_CHECKING:
    from bot.bot import Gorenmu
from bot.models import Status

__all__ = (
        'IsAfkCmd'
)

BaseDeco = BaseDecorators.IsAfk


class IsAfkCmd(commands.CustomComponent):
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
    @commands.command(name='isafk', aliases=[])
    async def isafk(self, ctx: Context, *, content: str, ) -> Response:
        translations = ctx.user.translations.IsAfk
        name = ctx.bot.StringTools.str2name(content.split()[0])
        actions = {ctx.bot.bot_nick: translations.bot_nick.format_response(ctx, success=False),
                   ctx.author.name: translations.author_nick.format_response(ctx, success=False)
                   }
        if name in actions:
            return actions[name]
        user = await User.get_or_none(name=name) if name != ctx.author.name.lower() else ctx.user
        if not user:
            return translations.never_seen.format_response(ctx, name)
        await user.fetch_related("status")
        if user.status[0].online:
            return translations.is_not_afk.format_response(ctx, name)
        afk: Status = user.status[0]
        status = ctx.user.translations.Afk.afks[afk.alias]
        if not afk.message:
            return translations.is_afk.format_response(ctx, name, status.current, status.emoji)
        return translations.is_afk.format_response(ctx, name, status.current, status.emoji, afk.message)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(IsAfkCmd(bot))


async def teardown(bot: Gorenmu) -> None:
    ...
