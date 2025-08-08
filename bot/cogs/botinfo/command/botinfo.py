# -*- coding: utf-8 -*-
from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from bot.ext import Context, commands
from bot.translations import Response

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class BotInfoCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: commands.Context) -> bool:  # NOQA
        return True

    @commands.base_decorator("BotInfo")
    @commands.command(name="botinfo", aliases=["info", "uptime", "site"])
    async def bot_info(self, ctx: Context) -> Response:
        translations = ctx.user.translations.BotInfo
        if ctx.invoked_with == "site":
            return translations.site.format_response(ctx, ctx.bot.config.BotConfig.site_url)
        if ctx.invoked_with == "uptime":
            timesince = ctx.user.translations.SupportTools.TimeTools.Humanize.precisedelta(
                datetime.now(UTC) - ctx.bot.boot
            )
            return translations.uptime.format_response(ctx, timesince)

        return translations.info.format_response(
            ctx,
            len(ctx.bot.channels),
            len(ctx.bot.commands),
            ctx.bot.config.BotConfig.dev_name,
            ctx.bot.config.BotConfig.site_url,
        )


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(BotInfoCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
