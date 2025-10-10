# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Context, Response, commands
from bot.utils import StringTools

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class EchoCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot)
        self.StringTools: StringTools = StringTools()

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: commands.Context) -> bool:  # NOQA
        return True

    @commands.command(name="echo", aliases=[])
    async def echo(self, ctx: Context, *, content) -> Response:
        return self.translations.Echo.echo(ctx, self.StringTools.start_remove_punctuation(content))


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(EchoCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
