# -*- coding: utf-8 -*-
import contextlib

from bot.ext.commands import Context
from bot.models import Status
from bot.translations import Response


async def listener(ctx: Context) -> Response | bool:
    translations = ctx.translations.Activity.Afk
    if (not ctx.bot.is_enabled(ctx, "afk") or not ctx.bot.channels[ctx.channel.name].online or
            ctx.command is not None and ctx.command.name in ["afk", "rafk"]):
        return False

    await ctx.user.fetch_related("status")
    with contextlib.suppress(IndexError):
        user_status: Status = (await ctx.user.status)[0]
    if not ctx.user or not ctx.user.status or user_status.online:
        return False
    status = translations.afks[user_status.alias]
    if user_status.message is None:
        response = translations.AfkListeners.is_afk.format_response(ctx, status.returned, status.emoji,
                                                                    user_status.updated_a_time, status.emoji
                                                                    )
    else:
        response = translations.AfkListeners.is_afk_content.format_response(ctx, status.returned, status.emoji,
                                                                            user_status.message,
                                                                            user_status.updated_a_time, status.emoji
                                                                            )

    user_status.online = True
    await user_status.save()
    afk_str = {"content": user_status.message, "updated_at": user_status.updated_at.isoformat(),
               "alias": user_status.alias}

    await ctx.bot.cache.set(f"{ctx.author.id}", afk_str, ttl=240, namespace="status")
    return response
