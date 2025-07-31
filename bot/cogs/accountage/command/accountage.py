# -*- coding: utf-8 -*-
from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from bot.ext import commands, Context
from bot.translations import Response

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class AccountAgeCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: commands.Context) -> bool:  # NOQA
        return True

    @commands.base_decorator("AccountAge")
    @commands.command(name="accountage", aliases=["age"])
    async def accountage(self, ctx: Context, user_name: str = "") -> Response:
        translations = ctx.user.translations
        user_name = ctx.bot.StringTools.str2name_or(user_name) or ctx.author.name.lower()
        user_tmi = await ctx.bot.fetch_user(login=user_name)
        if not user_tmi:
            return translations.Exceptions.user_not_found_name.format_response(ctx, user_name, success=False)

        mention = translations.SupportTools.LanguageContext.build_mention(ctx.author.name, user_name)
        now = datetime.datetime.now(tz=datetime.UTC)
        delta = translations.SupportTools.TimeTools.Humanize.precisedelta(user_tmi.created_at - now)
        date = user_tmi.created_at.strftime("%d/%m/%Y %H:%M:%S")

        return translations.AccountAge.age.format_response(ctx, mention, date, delta)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(AccountAgeCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
