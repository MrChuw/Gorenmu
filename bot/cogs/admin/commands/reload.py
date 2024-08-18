# -*- coding: utf-8 -*-
from bot.ext.commands import base_decorator, Bucket, check, command, Context, cooldown
from bot.translations import EnUsDecorators, Response
from bot.utils import Check, Role


@base_decorator(EnUsDecorators.Admin.Reload)
@cooldown(rate=3, per=10, bucket=Bucket.user)
@check([Role.dev])
@command(name='reload', aliases=[])
async def command(ctx: Context) -> Response:
    ctx.bot.CommandHandler.reload_cogs(ctx.bot)
    return ctx.translations.Admin.Reload().commands_reloaded.format_response(ctx)
