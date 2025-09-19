# -*- coding: utf-8 -*-
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from bot.ext import Context, Response, commands
from bot.ext.named_tuples import RAfkNamedTuple
from bot.models import Status

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu

afk_alias = [
    "read",
    "brb",
    "eat",
    "food",
    "play",
    "game",
    "sleep",
    "night",
    "study",
    "art",
    "watch",
    "shower",
    "code",
    "work",
]


class AFKCmd(commands.CustomComponent):
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

    @commands.command(name="afk", aliases=afk_alias)
    async def afk(self, ctx: Context, *, content: str = "") -> Response:
        if len(content) >= 450:
            return self.translations.Exceptions.too_much_characters(ctx)
        afk = self.translations.AFK.afks(ctx).get(ctx.invoke_by)  # NOQA
        await Status.go_afk(ctx=ctx, status=afk, content=content)
        if not content:
            return self.translations.AFK.afk(ctx, afk.leave, afk.emoji)
        return self.translations.AFK.content(ctx, afk.leave, afk.emoji, content)

    @commands.event_handler("event_message")
    async def return_from_afk(self, ctx: Context) -> Response | bool:
        translations = self.translations
        if (
            not ctx.bot.CommandHandler.is_enabled(ctx, "afk")
            or not ctx.bot.channels[ctx.channel.name].online
            or ctx.command is not None
            and ctx.command.name in ["afk", "rafk"]
        ):
            return False
        user_status: Status = await Status.get_afk(ctx)
        if not ctx.user or user_status.online:
            return False
        status = translations.AFK.afks(ctx).get(user_status.alias)
        humanize = translations.SupportTools.TimeTools.Humanize(ctx)
        a_time = humanize.created_a_time(user_status.updated_at, ctx.user.timezone_)
        clock_emojis = {
            0.0: "🕛",
            0.5: "🕧",
            1.0: "🕐",
            1.5: "🕜",
            2.0: "🕑",
            2.5: "🕝",
            3.0: "🕒",
            3.5: "🕞",
            4.0: "🕓",
            4.5: "🕟",
            5.0: "🕔",
            5.5: "🕠",
            6.0: "🕕",
            6.5: "🕡",
            7.0: "🕖",
            7.5: "🕢",
            8.0: "🕗",
            8.5: "🕣",
            9.0: "🕘",
            9.5: "🕤",
            10.0: "🕙",
            10.5: "🕥",
            11.0: "🕚",
            11.5: "🕦",
        }
        delta = datetime.now(ctx.user.timezone_) - user_status.updated_at.astimezone(ctx.user.timezone_)
        rounded_hours = round(((delta.total_seconds() / 3600) % 12) * 2) / 2
        clock_emoji = clock_emojis.get(rounded_hours, "🕛")

        if user_status.message is None or user_status.message == "":
            response = translations.AFKReturn.afk(ctx, status.returned, status.emoji, a_time, clock_emoji)
        else:
            response = translations.AFKReturn.content(
                ctx, status.returned, status.emoji, user_status.message, a_time, clock_emoji
            )

        user_status.online = True
        await user_status.save()
        afk_tuple = RAfkNamedTuple(
            content=user_status.message, updated_at=user_status.updated_at, alias=user_status.alias, afk=user_status
        )

        await ctx.bot.memcache.RAfk.set(user=ctx.user, value=afk_tuple)
        return response


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(AFKCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
