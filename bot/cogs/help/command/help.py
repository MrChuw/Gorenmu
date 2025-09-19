# -*- coding: utf-8 -*-
from __future__ import annotations

import difflib
from typing import TYPE_CHECKING

from twitchio.ext import commands as twitchio_commands

from bot.ext import Context, commands
from bot.translations import Response

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class HelpCmd(commands.CustomComponent):
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

    @commands.command(name="help", aliases=[])
    async def help(self, ctx: Context, *, content: str = "") -> Response:
        translations = self.translations.Help
        site_url = ctx.bot.config.BotConfig.site_url
        parts = content.split(" ")
        if not content:
            # TODO: upload to bin.mrchuw
            return translations.command_site(ctx, site_url)
        command = ctx.bot.get_command(parts[0])

        if len(parts) != 1 and isinstance(command, twitchio_commands.Group):
            command = command.get_command(parts[1])

        if not command:
            commands_list = ctx.bot.commands.keys()
            suggested_command = difflib.get_close_matches(content, commands_list, n=1, cutoff=0.6)
            return translations.suggested_command(ctx, content, suggested_command[0])

        aliases = ", ".join(command.aliases) if command.aliases else ""
        decorator = command.component.translations.get_decorator(command)
        url = site_url / "commands" / command.qualified_name  # TODO: Change.
        if hasattr(command, "per"):
            cooldown = self.translations.SupportTools.TimeTools.Humanize(ctx).naturaldelta(command.per / command.rate)
        else:
            cooldown = "None"
        return translations.help(ctx, ctx.prefix, command.name, decorator.deco_helper(ctx), cooldown, url, aliases)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(HelpCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
