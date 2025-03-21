# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import commands, Context
from bot.models import MessagesLog, User
from bot.translations import BaseDecorators, Response

if TYPE_CHECKING:
    from bot.bot import Gorenmu


# TODO: Test with a big message database


class RandomLineCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot

    cooldown_rate = 1
    cooldown_per = 5
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None:
        ...

    @commands.Component.guard()
    def guards_component(self, ctx: commands.Context) -> bool:
        return True

    @commands.base_decorator(BaseDecorators.RandomLine)
    @commands.command(name='randomline', aliases=['rl'])
    async def randomline(self, ctx: Context, *, options: str = "") -> Response:
        translations = ctx.user.translations
        humanize = ctx.user.translations.SupportTools.TimeTools.Humanize
        options_split = options.split(" ")
        channel_original = self.bot.ToolsTools.find_prefixed_option(options_split, "channel:")
        user_original = self.bot.ToolsTools.find_prefixed_option(options_split, "user:")
        user, channel = None, None
        if user_original:
            if user_original.lower() != ctx.author.name.lower():
                user = await User.get_user(ctx, user_original)
            else:
                user = ctx.user
            if isinstance(user, Response):
                return user

        if channel_original and channel_original != "global":
            channel = ctx.bot.channels.get(channel_original)
            if not channel:
                return translations.Exceptions.channel_not_found.format_response(ctx, channel_original)

        if channel is None and channel_original != "global":
            channel = ctx.bot.channels.get(ctx.channel.name)

        message, count = await MessagesLog.get_random_message(user=user, channel=channel)
        message: MessagesLog
        if count == 0:
            return translations.RandomLine.no_message_found.format_response(
                    ctx,
                    user_original or "",
                    channel_original or ctx.channel.name
            )
        if not count:
            return translations.RandomLine.search_timeout.format_response(
                    ctx,
                    user_original or "",
                    channel_original or ctx.channel.name
            )
        return translations.RandomLine.random_line.format_response(
                ctx,
                message.content,
                humanize.created_a_time(created_at=message.created_at, timezone=ctx.user.timezone_),
                message.user.nickname or message.user.name
        )


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(RandomLineCmd(bot))


async def teardown(bot: Gorenmu) -> None:
    ...
