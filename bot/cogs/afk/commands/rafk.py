from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Context, Response, commands
from bot.models import Status

from .translations import Translations, rafk_alias

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class RAfkCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot, self)

    @commands.command(name=rafk_alias[0], aliases=rafk_alias[1:], pipeble=False)
    async def rafk(self, ctx: Context, *, content: str = "") -> Response:
        rafk = await self.bot.memcache.RAfk.get(user_id=ctx.author.id)
        if rafk is None:
            return self.translations.Exceptions.time_expired(self.translations.RAFK.return_expired())

        status = self.translations.AFK.afks()[rafk.alias]
        if content:
            rafk.content = content
        await Status.go_rafk(ctx, rafk)
        if rafk.content == "":
            return self.translations.AFK.afk(status.leave_again, status.emoji)
        else:
            return self.translations.RAFK.content(status.leave_again, status.emoji, rafk.content)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(RAfkCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
