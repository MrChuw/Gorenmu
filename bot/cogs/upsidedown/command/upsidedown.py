# -*- coding: utf-8 -*-
from bot.apis.upsidedown import transform
from bot.bot import Gorenmu
from bot.ext.commands import base_decorator, Bucket, check, command, Command, Context, cooldown
from bot.translations import BaseDecorators, Response


@base_decorator(BaseDecorators.UpSideDown)
@cooldown(rate=3, per=10, bucket=Bucket.user)
@check([])
@command(name='upsidedown', aliases=['updown'])
async def command(ctx: Context, *, content, ) -> Response:
    return ctx.translations.UpSideDown.upsidedown.format_response(ctx, transform(content))

