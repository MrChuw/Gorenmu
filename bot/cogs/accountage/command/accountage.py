from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from bot.ext import Context, Response, commands
from bot.utils import StringTools

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class AccountAgeCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.StringTools = StringTools()
        self.translations: Translations = Translations(bot, self)

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    async def component_before_invoke(self, ctx: Context) -> None:
        self.translations.ctx_set(ctx)

    @commands.Component.guard()
    def guards_component(self, ctx: commands.Context) -> bool:  # NOQA
        return True

    @commands.command(name="accountage", aliases=["age"])
    async def accountage(self, ctx: Context, user_name: str = "") -> Response:
        user_name = self.StringTools.str2name_or(user_name or ctx.author.name)
        if not (user_tmi := await ctx.bot.fetch_user(login=user_name)):
            return self.translations.Exceptions.user_not_found_name(user_name)
        timetools = self.translations.SupportTools.TimeTools
        mention = self.translations.SupportTools.LanguageContext.mention(ctx.author.name, user_name)
        now = datetime.datetime.now(tz=datetime.UTC)
        delta = timetools.Humanize(ctx.user.language).precisedelta(user_tmi.created_at - now)
        date = user_tmi.created_at.strftime(timetools.strftime())

        return self.translations.AccountAge.accountage(mention, date, delta)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(AccountAgeCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
