from __future__ import annotations

from typing import TYPE_CHECKING

from bot.apis import BestLogs
from bot.ext import Context, Response, commands
from bot.utils import SessionsCaches, StringTools

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class RandomLineCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot, self)
        self.StringTools: StringTools = StringTools()
        self.SessionsCaches: SessionsCaches = SessionsCaches(bot)
        self.BestLogs: BestLogs = BestLogs(bot, self.SessionsCaches.RandomLine.session)

    @commands.command(name="randomline", aliases=["rl"])
    async def randomline(self, ctx: Context, *, options: str = "") -> Response:
        translations = self.translations
        humanize = self.translations.SupportTools.TimeTools.Humanize(ctx.user.language)
        options_split = options.split(" ")
        channel = self.StringTools.find_prefixed_option(options_split, "channel:")
        user = self.StringTools.find_prefixed_option(options_split, "user:")
        messages = await self.BestLogs.RustLogs.get_random_message(ctx, channel or ctx.channel_name, user, random=True)
        if messages == "No user logs found" or messages is None:
            if not channel and user:
                return translations.RandomLine.no_user_message(user)
            if not user and channel:
                return translations.RandomLine.no_channel_message(channel)
            if user and channel:
                return translations.RandomLine.no_user_on_channel(user, channel or ctx.channel_name)
            return translations.RandomLine.error()
        message = messages.get_random()
        return translations.RandomLine.random_line(
            message.text or "",
            humanize.created_a_time(created_at=message.timestamp, timezone=await ctx.user.tz(self.bot)),
            message.username or "",
        )


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(RandomLineCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
