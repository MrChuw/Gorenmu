# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import commands, Context
from bot.translations import Response

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class PipeCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: Context) -> bool:  # NOQA
        return True

    @commands.base_decorator("Pipe")  # TODO: change when site is ready
    @commands.command(name="pipe", aliases=[])
    async def pipe(self, ctx: Context) -> Response:
        if ctx.user.language == ctx.bot.TranslationManager.languages[0]:
            url = f"{ctx.bot.config.BotConfig.site_url}{ctx.bot.TranslationManager.languages[0]}/commands/pipe.html"
        elif ctx.user.language == ctx.bot.TranslationManager.languages[1]:
            url = f"{ctx.bot.config.BotConfig.site_url}{ctx.bot.TranslationManager.languages[1]}/comandos/pipe.html"

        else:
            url = f"{ctx.bot.config.BotConfig.site_url}{ctx.bot.TranslationManager.languages[0]}/commands/pipe.html"
        return ctx.user.translations.Pipe.response.format_response(ctx, url)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(PipeCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
