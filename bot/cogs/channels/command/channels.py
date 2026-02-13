from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Context, Response, commands
from bot.utils import Role, StringTools

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class ChannelsCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot, self)
        self.StringTools: StringTools = StringTools()

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    async def component_before_invoke(self, ctx: Context) -> None:
        self.translations.ctx_set(ctx)

    @commands.Component.guard()
    def guards_component(self, ctx: commands.Context) -> bool:  # NOQA
        return Role.admin(ctx)

    @commands.command(name="channels", aliases=[])
    async def channels(self, ctx: Context, extras=None) -> Response:
        translations = self.translations.Channels
        if extras == "quantity":
            return translations.quantity(len(ctx.bot.channels))
        if extras == "ping":
            channels = ", ".join(f"@{channel}" for channel in ctx.bot.channels)
            return translations.names(channels)
        inv = self.StringTools.inv_char()
        channels = ", ".join(f"@{channel}{inv}" for channel in ctx.bot.channels)
        return translations.names(channels)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(ChannelsCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
