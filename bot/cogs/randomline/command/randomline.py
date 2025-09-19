# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Context, commands
from bot.models import MessagesLog, User
from bot.translations import Response
from bot.utils import SessionsCaches, StringTools, TimeTools, UploadThings

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class RandomLineCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot)
        self.StringTools: StringTools = StringTools()

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
        channel_original = self.StringTools.find_prefixed_option(options_split, "channel:")
        user_original = self.StringTools.find_prefixed_option(options_split, "user:")
        user, channel = None, None
        if user_original:
            if user_original.lower() != ctx.author.name.lower():
                user = await User.get_user(ctx, name=user_original, translations=self.translations)
            else:
                user = ctx.user
            if hasattr(user, "response_string"):
                return user

        if channel_original and channel_original != "global":
            channel = ctx.bot.channels.get(channel_original)
            if not channel:
                return translations.Exceptions.channel_not_found(ctx, channel_original)

        if channel is None and channel_original != "global":
            channel = ctx.bot.channels.get(ctx.channel.name)

        message, count = await MessagesLog.get_random_message(user=user, channel=channel)
        message: MessagesLog
        if count == 0:
            if not channel and user:
                return translations.RandomLine.no_user_message(ctx, user_original)
            elif channel and not user:
                return translations.RandomLine.no_channel_message(ctx, channel_original or ctx.channel.name)

            return translations.RandomLine.no_user_on_channel(ctx, user_original, channel_original or ctx.channel.name)
        if not count:
            return translations.RandomLine.search_timeout(
                ctx, user_original or "", channel_original or ctx.channel.name
            )
        return translations.RandomLine.random_line(
            ctx,
            message.content,
            humanize.created_a_time(created_at=message.created_at, timezone=ctx.user.timezone_),
            message.user.nickname or message.user.name,
        )


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(RandomLineCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
