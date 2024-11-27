# -*- coding: utf-8 -*-
from bot.bot import Gorenmu
from bot.ext.commands import base_decorator, Bucket, check, command, Command, Context, cooldown
from bot.translations import BaseDecorators, Response


@base_decorator(BaseDecorators.Reverse)
@cooldown(rate=3, per=10, bucket=Bucket.user)
@check([])
@command(name='reverse', aliases=["invert"])
async def command(ctx: Context, *, content, ) -> Response:
    return ctx.translations.Reverse().reversed_string.format_response(ctx, content[::-1])

