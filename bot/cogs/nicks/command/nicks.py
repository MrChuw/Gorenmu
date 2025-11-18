# -*- coding: utf-8 -*-
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from bot.apis import BestLogs
from bot.ext import Context, Response, commands
from bot.utils import Check, Role, SessionsCaches, StringTools

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class NicksCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot)
        self.StringTools: StringTools = StringTools()
        self.SessionsCaches: SessionsCaches = SessionsCaches(bot)
        self.SessionsCaches: SessionsCaches = SessionsCaches(bot)
        self.BestLogs: BestLogs = BestLogs(bot, self.SessionsCaches.RandomLine.session)

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: commands.Context) -> bool:  # NOQA
        return True

    @commands.command(name="nicks", aliases=["nickhistory", "namehistory"])
    async def nicks(self, ctx: Context, name: str) -> Response:
        name = self.StringTools.str2name(name)
        nicks = await self.BestLogs.ZonianLogs.name_history(ctx, user=name)
        if not nicks:
            return self.translations.Nicks.not_seen(ctx, name)
        ordered = [h for h in nicks if h.first_timestamp is not None]
        ordered.sort(key=lambda h: (h.first_timestamp, h.last_timestamp or datetime.max))
        sequence = [h.user_login for h in ordered]
        return self.translations.Exceptions.echo(ctx, " → ".join(sequence))


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(NicksCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
