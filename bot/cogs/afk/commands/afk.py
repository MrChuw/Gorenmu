from __future__ import annotations

import json
from datetime import datetime
from typing import TYPE_CHECKING

from bot.ext import Context, Response, commands
from bot.models import Status
from bot.types.named_tuples import RAfkNamedTuple

from .translations import Translations, afk_keys

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class AFKCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot, self)


    @commands.command(name=afk_keys[0], aliases=afk_keys[1:])
    async def afk(self, ctx: Context, *, content: str = "") -> Response:
        if len(content) >= 450:
            return self.translations.Exceptions.too_much_characters(ctx)
        afk = self.translations.AFK.afks().get(ctx.invoke_by)
        if not afk:
            exception = Exception(f"Error in get status for {json.dumps(ctx.invoke_by, indent=2)}.")
            await self.bot.CommandHandler.send_bug(ctx, exception)
            return self.translations.Exceptions.error_not_registered(dev=self.bot.dev_user.display_name or "")
        await Status.go_afk(ctx=ctx, status=afk, content=content)
        if not content:
            return self.translations.AFK.afk(afk.leave, afk.emoji)
        return self.translations.AFK.content(afk.leave, afk.emoji, content)

    @commands.event_handler("event_message")
    async def return_from_afk(self, ctx: Context) -> Response | bool:
        translations = self.translations
        if (
            not await ctx.bot.CommandHandler.is_enabled(ctx, "afk")
            or not ctx.bot.channels.is_online(ctx)
            or (ctx.command is not None and ctx.command.name in ["afk", "rafk"])
        ):
            return False
        user_status: Status = await Status.get_afk(ctx)
        if not ctx.user or user_status.online:
            return False
        status = translations.AFK.afks().get(user_status.alias)
        if not status:
            exception = Exception(f"Error in get status for {json.dumps(user_status, indent=2)}.")
            await self.bot.CommandHandler.send_bug(ctx, exception)
            return self.translations.Exceptions.error_not_registered(dev=self.bot.dev_user.display_name or "")
        humanize = translations.SupportTools.TimeTools.Humanize(ctx.user.language)
        a_time = humanize.created_a_time(user_status.updated_at, await ctx.user.tz(self.bot))
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
        delta = datetime.now(await ctx.user.tz(self.bot)) - user_status.updated_at.astimezone(
            await ctx.user.tz(self.bot)
        )
        rounded_hours = round(((delta.total_seconds() / 3600) % 12) * 2) / 2
        clock_emoji = clock_emojis.get(rounded_hours, "🕛")

        if user_status.message is None or user_status.message == "":
            response = translations.AFKReturn.afk(status.returned, status.emoji, a_time, clock_emoji)
        else:
            response = translations.AFKReturn.content(
                status.returned,
                status.emoji,
                user_status.message,
                a_time,
                clock_emoji,
            )

        user_status.online = True
        await user_status.save()
        afk_tuple = RAfkNamedTuple(
            content=user_status.message or "",
            updated_at=user_status.updated_at,
            alias=user_status.alias,
            afk=user_status,
        )

        await ctx.bot.memcache.RAfk.set(user=ctx.user, value=afk_tuple)
        return response


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(AFKCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
