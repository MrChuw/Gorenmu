# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Context, Response, commands
from bot.utils import SessionsCaches, StringTools, TimeTools, UploadThings

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class ReverseCmd(commands.CustomComponent):
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

    @commands.command(name="reverse", aliases=["invert"])
    async def reverse(self, ctx: Context, *, content) -> Response:
        return self.translations.Exceptions.echo(ctx, content[::-1])


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(ReverseCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
