from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Context, Response, commands
from bot.models import Status

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu

rafk_alias = [
    f"r{s}"
    for s in [
        "read",
        "brb",
        "eat",
        "food",
        "play",
        "game",
        "sleep",
        "night",
        "study",
        "art",
        "watch",
        "shower",
        "code",
        "work",
    ]
]


class RAfkCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot, self)

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    async def component_before_invoke(self, ctx: Context) -> None:
        self.translations.ctx_set(ctx)

    @commands.Component.guard()
    def guards_component(self, ctx: Context) -> bool:  # NOQA
        return True

    @commands.command(name="rafk", aliases=rafk_alias, pipeble=False)
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
