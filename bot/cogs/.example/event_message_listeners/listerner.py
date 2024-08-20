# -*- coding: utf-8 -*-
import contextlib

from bot.ext.commands import Context
from bot.translations import Response


async def listener(ctx: Context) -> Response | bool:
    translations = ctx.translations
    if (not ctx.bot.is_enabled(ctx, "afk") or not ctx.bot.channels[
        ctx.channel.name].online or ctx.command is not None and ctx.command.name in ["afk", "rafk"]):
        return False
