from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Context, Response, commands
from bot.models import User
from bot.utils import StringTools

if TYPE_CHECKING:
    from bot.bot import Gorenmu

from bot.models import Status

from .translations import Translations


class IsAfkCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot, self)
        self.StringTools = StringTools()

    @commands.command(name="isafk", aliases=[])
    async def isafk(self, ctx: Context, name: str) -> Response:
        author_name = ctx.author.name or ""
        name = self.StringTools.str2name(name or author_name)
        actions = {
            str(ctx.bot.bot_user.display_name or "").lower(): self.translations.IsAFK.bot(),
            author_name.lower(): self.translations.IsAFK.author(),
        }
        if name.lower() in actions:
            return actions[name.lower()]
        user = (
            await User.get_user_or_none(ctx_bot=ctx, translations=self.translations, name=name)
            if name != author_name.lower()
            else ctx.user
        )
        if not user:
            return self.translations.Exceptions.never_seen(name)
        afk = await Status.get_afk(ctx=ctx, user=user)
        if afk.online:
            return self.translations.IsAFK.is_not_afk(name)
        status = self.translations.AFK.afks()[afk.alias]
        time = self.translations.SupportTools.TimeTools.Humanize(ctx.user.language).updated_a_time(afk.updated_at)
        if not afk.message:
            return self.translations.IsAFK.is_afk(name, status.current, status.emoji, time)
        return self.translations.IsAFK.is_afk_content(name, status.current, status.emoji, afk.message, time)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(IsAfkCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
