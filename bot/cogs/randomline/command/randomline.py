# -*- coding: utf-8 -*-
from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from bot.apis import BestLogs
from bot.ext import Context, Response, commands
from bot.models import MessagesLog, User
from bot.utils import SessionsCaches, StringTools, TimeTools, UploadThings

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class RandomLineCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot)
        self.StringTools: StringTools = StringTools()
        self.SessionsCaches: SessionsCaches = SessionsCaches(bot)
        self.BestLogs: BestLogs = BestLogs(bot, self.SessionsCaches.RandomLine.session)

    cooldown_rate = 1
    cooldown_per = 5
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: Context) -> bool:  # NOQA
        return True

    @commands.command(name="randomline", aliases=["rl"])
    async def randomline(self, ctx: Context, *, options: str = "") -> Response:
        translations = self.translations
        humanize = self.translations.SupportTools.TimeTools.Humanize(ctx)
        options_split = options.split(" ")
        channel = self.StringTools.find_prefixed_option(options_split, "channel:")
        user = self.StringTools.find_prefixed_option(options_split, "user:")
        messages = await self.BestLogs.RustLogs.get_random_message(ctx, channel or ctx.channel.name, user)
        if messages == "No user logs found":
            if not channel and user:
                return translations.RandomLine.no_user_message(ctx, user)
            elif channel and not user:
                return translations.RandomLine.no_channel_message(ctx, channel or ctx.channel.name)
            return translations.RandomLine.no_user_on_channel(ctx, user, channel or ctx.channel.name)
        message = messages.messages[0]
        return translations.RandomLine.random_line(
            ctx,
            message.text,
            humanize.created_a_time(created_at=message.timestamp, timezone=ctx.user.timezone_),
            message.username,
        )


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(RandomLineCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
