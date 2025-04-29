# -*- coding: utf-8 -*-
from bot.ext.commands import Context
from bot.models import Status
from bot.translations import Response
from datetime import datetime


async def event_message(ctx: Context) -> Response | bool:
    translations = ctx.user.translations.AfkListeners
    if (not ctx.bot.is_enabled(ctx, "afk") or not ctx.bot.channels[ctx.channel.name].online or
            ctx.command is not None and ctx.command.name in ["afk", "rafk"]):
        return False
    user_status: Status = await Status.get_afk(ctx, namespace="afk")
    if not ctx.user or user_status.online:
        return False
    status = ctx.user.translations.Afk.afks[user_status.alias]
    humanize = ctx.user.translations.SupportTools.TimeTools.Humanize
    a_time = humanize.created_a_time(user_status.updated_at, ctx.user.timezone_)
    clock_emojis = {
            0.0: "🕛", 0.5: "🕧",
            1.0: "🕐", 1.5: "🕜",
            2.0: "🕑", 2.5: "🕝",
            3.0: "🕒", 3.5: "🕞",
            4.0: "🕓", 4.5: "🕟",
            5.0: "🕔", 5.5: "🕠",
            6.0: "🕕", 6.5: "🕡",
            7.0: "🕖", 7.5: "🕢",
            8.0: "🕗", 8.5: "🕣",
            9.0: "🕘", 9.5: "🕤",
            10.0: "🕙", 10.5: "🕥",
            11.0: "🕚", 11.5: "🕦",
    }
    delta = datetime.now(ctx.user.timezone_) - user_status.updated_at.astimezone(ctx.user.timezone_)
    hours = delta.total_seconds() / 3600
    hours %= 12
    rounded_hours = round(hours * 2) / 2
    clock_emoji = clock_emojis.get(rounded_hours, "🕛")

    if user_status.message is None or user_status.message == "":
        response = translations.is_afk.format_response(
                ctx,
                status.returned,
                status.emoji,
                a_time,
                clock_emoji
        )
    else:
        response = translations.is_afk_content.format_response(
                ctx,
                status.returned,
                status.emoji,
                user_status.message,
                a_time,
                clock_emoji
        )

    user_status.online = True
    await user_status.save()
    afk_str = {
            "content": user_status.message,
            "updated_at": user_status.updated_at,
            "alias": user_status.alias
            }

    await ctx.bot.memcache.set(int(ctx.author.id), afk_str, ttl=240, namespace="rafk")
    return response





