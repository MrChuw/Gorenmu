# -*- coding: utf-8 -*-
from __future__ import annotations

import difflib
from typing import TYPE_CHECKING

from bot.ext import commands, Context
from bot.translations import Response

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class HelpCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: commands.Context) -> bool:  # NOQA
        return True

    @commands.base_decorator("Help")
    @commands.command(name="help", aliases=[])
    async def help(self, ctx: Context, *, content: str = "") -> Response:
        translations = ctx.user.translations.Help
        site_url = ctx.bot.config.BotConfig.site_url
        if not content:
            # TODO: upload to bin.mrchuw
            return translations.command_site.format_response(ctx, site_url, success=False)
        command = ctx.bot.get_command(content)

        if not command:
            commands_list = ctx.bot.commands.keys()
            suggested_command = difflib.get_close_matches(content, commands_list, n=1, cutoff=0.6)
            return translations.suggested_command.format_response(ctx, content, suggested_command[0], success=False)

        aliases = ", ".join(command.aliases) if command.aliases else ""
        decorator = ctx.bot.TranslationManager.get_decorator(command, ctx)
        url = site_url / "commands" / command.qualified_name  # TODO: Change.
        cooldown = ctx.user.translations.SupportTools.TimeTools.Humanize.naturaldelta(command.per / command.rate)

        return translations.help.format_response(
            ctx, ctx.prefix, command.name, decorator.helper, cooldown, url, aliases
        )


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(HelpCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
