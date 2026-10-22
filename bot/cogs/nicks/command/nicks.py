from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from bot.apis import BestLogs
from bot.ext import Context, Response, commands
from bot.utils import SessionsCaches, StringTools

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class NicksCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot, self)
        self.StringTools: StringTools = StringTools()
        self.SessionsCaches: SessionsCaches = SessionsCaches(bot)
        self.BestLogs: BestLogs = BestLogs(bot, self.SessionsCaches.RandomLine.session)

    @commands.command(name="nicks", aliases=["nickhistory", "namehistory"])
    async def nicks(self, ctx: Context, name: str, *args: str) -> Response:
        name = self.StringTools.str2name(name)
        time, _ = self.StringTools.unpack_dynamic(args, 1)
        nicks = await self.BestLogs.ZonianLogs.name_history(ctx, user=name)

        if not nicks:
            return self.translations.Nicks.not_seen(name)
        if isinstance(nicks, str):
            return self.translations.Exceptions.echo(nicks)

        ordered = [h for h in nicks if h.first_timestamp is not None]
        ordered.sort(key=lambda h: (h.first_timestamp, h.last_timestamp or datetime.max))
        if len(ordered) == 1 and time:
            h = ordered[0]
            if h.user_login:
                date_fmt = "%Y-%m-%d %H:%M"
                first_str = h.first_timestamp.astimezone(await ctx.user.tz(self.bot)).strftime(date_fmt)
                last_str = (
                    h.last_timestamp.astimezone(await ctx.user.tz(self.bot)).strftime(date_fmt)
                    if h.last_timestamp
                    else "presente"
                )
                return self.translations.Exceptions.echo(f"{h.user_login} ({first_str} → {last_str})")

        sequence = []
        for h in ordered:
            if not h.user_login:
                continue

            if time and h.last_timestamp:
                formatted_date = h.last_timestamp.astimezone(await ctx.user.tz(self.bot)).strftime("%Y-%m-%d %H:%M")
                sequence.append(f"{h.user_login} ({formatted_date})")
            else:
                sequence.append(h.user_login)

        return self.translations.Exceptions.echo(" → ".join(sequence))


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(NicksCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
