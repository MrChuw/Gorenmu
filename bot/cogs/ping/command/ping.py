from __future__ import annotations

import datetime
import os
from typing import TYPE_CHECKING

import psutil

from bot.ext import Context, Response, commands

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class PingCmd(commands.CustomComponent):
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

    @commands.command(name="ping", aliases=["pong"])
    async def ping(self, ctx: Context) -> Response:
        translations = self.translations.Ping
        humanize = self.translations.SupportTools.TimeTools.Humanize(ctx)
        delta = datetime.datetime.now(datetime.UTC) - ctx.message.timestamp
        tmi = f"{humanize.precisedelta(delta, suppress=['seconds'], minimum_unit='milliseconds').split(' ')[0]} ms"
        mem = humanize.naturalsize(psutil.Process(os.getpid()).memory_info()[0])
        started = humanize.precisedelta(ctx.bot.boot - datetime.datetime.now(datetime.UTC))
        return translations.ping(ctx, "ping 🏓" if ctx.invoke_by == "pong" else "pong 🏓", tmi, mem, started)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(PingCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
