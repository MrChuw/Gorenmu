# -*- coding: utf-8 -*-
from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from bot.ext import Context, Response, commands

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class BotInfoCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot)

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: commands.Context) -> bool:  # NOQA
        return True

    @commands.command(name="botinfo", aliases=["info", "uptime", "site"])
    async def bot_info(self, ctx: Context) -> Response:
        translations = self.translations.BotInfo
        if ctx.invoked_with == "site":
            return translations.site(ctx, ctx.bot.config.BotConfig.site_url)
        if ctx.invoked_with == "uptime":
            timesince = self.translations.SupportTools.TimeTools.Humanize(ctx).precisedelta(
                datetime.now(UTC) - ctx.bot.boot
            )
            return translations.uptime(ctx, timesince)

        return translations.info(
            ctx,
            len(ctx.bot.channels),
            len(ctx.bot.commands),
            ctx.bot.config.BotConfig.dev_name,
            ctx.bot.config.BotConfig.site_url,
        )


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(BotInfoCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
