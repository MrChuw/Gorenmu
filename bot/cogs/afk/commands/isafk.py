# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Context, commands
from bot.models import User
from bot.translations import Response
from bot.utils import StringTools

if TYPE_CHECKING:
    from bot.bot import Gorenmu

from bot.models import Status

from .translations import Translations


class IsAfkCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot)
        self.StringTools = StringTools()

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: Context) -> bool:  # NOQA
        return True

    @commands.command(name="isafk", aliases=[])
    async def isafk(self, ctx: Context, *, content: str) -> Response:
        name = self.StringTools.str2name(content.split()[0])
        actions = {
            ctx.bot.bot_nick: self.translations.IsAFK.bot(ctx),
            ctx.author.name: self.translations.IsAFK.author(ctx),
        }
        if name in actions:
            return actions[name]
        user = (
            await User.get_user(ctx=ctx, name=name, is_none=True, translations=self.translations)
            if name != ctx.author.name.lower()
            else ctx.user
        )
        if not user:
            return self.translations.Exceptions.never_seen(ctx, name)
        afk = await Status.get_afk(ctx=ctx, user=user)
        if afk.online:
            return self.translations.IsAFK.is_not_afk(ctx, name)
        status = self.translations.AFK.afks(ctx)[afk.alias]
        time = self.translations.SupportTools.TimeTools.Humanize(ctx).updated_a_time(afk.updated_at)
        if not afk.message:
            return self.translations.IsAFK.is_afk(ctx, name, status.current, status.emoji, time)
        return self.translations.IsAFK.is_afk_content(ctx, name, status.current, status.emoji, afk.message, time)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(IsAfkCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
