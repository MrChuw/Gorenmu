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
        self.translations: Translations = Translations(bot, self)

    @commands.command(name="ping", aliases=["pong"])
    async def ping(self, ctx: Context) -> Response:
        translations = self.translations.Ping
        humanize = self.translations.SupportTools.TimeTools.Humanize(ctx.user.language)
        timestamp = ctx.message.timestamp if ctx.message else datetime.datetime.now(datetime.UTC)  # NOQA
        delta = datetime.datetime.now(datetime.UTC) - (timestamp or datetime.datetime.now(datetime.UTC))
        tmi = f"{humanize.precisedelta(delta, suppress=['seconds'], minimum_unit='milliseconds').split(' ')[0]} ms"
        mem = humanize.naturalsize(psutil.Process(os.getpid()).memory_info()[0])
        started = humanize.precisedelta(ctx.bot.boot - datetime.datetime.now(datetime.UTC))
        return translations.ping("ping 🏓" if ctx.invoke_by == "pong" else "pong 🏓", tmi, mem, started)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(PingCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
