# -*- coding: utf-8 -*-
from bot.ext.commands import Context
from bot.models import Status
from bot.translations import Response
from datetime import datetime, UTC


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
    a_time = humanize.precisedelta(datetime.now(UTC) - user_status.updated_at.astimezone(UTC))
    if user_status.message is None:
        response = translations.is_afk.format_response(
                ctx,
                status.returned,
                status.emoji,
                a_time,
                status.emoji
        )
    else:
        response = translations.is_afk_content.format_response(
                ctx,
                status.returned,
                status.emoji,
                user_status.message,
                a_time,
                status.emoji
        )

    user_status.online = True
    await user_status.save()
    afk_str = {"content": user_status.message, "updated_at": user_status.updated_at.isoformat(),
               "alias": user_status.alias}

    await ctx.bot.cache.set(int(ctx.author.id), afk_str, ttl=240, namespace="rafk")

    # await ctx.bot.cache.set(f"{ctx.author.id}", afk_str, ttl=240, namespace="status")
    return response

























