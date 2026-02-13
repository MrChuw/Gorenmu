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

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    async def component_before_invoke(self, ctx: Context) -> None:
        self.translations.ctx_set(ctx)

    @commands.Component.guard()
    def guards_component(self, ctx: Context) -> bool:  # NOQA
        return True

    @commands.command(name="isafk", aliases=[])
    async def isafk(self, ctx: Context, *, content: str) -> Response:
        name = self.StringTools.str2name(content.split()[0])
        actions = {
            ctx.bot.bot_user.display_name.lower(): self.translations.IsAFK.bot(),
            ctx.author.name.lower(): self.translations.IsAFK.author(),
        }
        if name.lower() in actions:
            return actions[name.lower()]
        user = (
            await User.get_user(ctx_bot=ctx, translations=self.translations, name=name, is_none=True)
            if name != ctx.author.name.lower()
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
