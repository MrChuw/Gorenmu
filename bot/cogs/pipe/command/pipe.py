# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Context, commands
from bot.translations import Response

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class PipeCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot)

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: Context) -> bool:  # NOQA
        return True

    @commands.command(name="pipe", aliases=[])  # TODO: change when site is ready
    async def pipe(self, ctx: Context) -> Response:
        if ctx.user.language:
            url = f"{ctx.bot.config.BotConfig.site_url}/{ctx.user.language.lower()}/commands/pipe.html"
        else:
            url = f"{ctx.bot.config.BotConfig.site_url}/en/commands/pipe.html"
        return self.translations.Pipe.pipe(ctx, url)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(PipeCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
