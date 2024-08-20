# -*- coding: utf-8 -*-
import random

from bot.ext.commands import base_decorator, Bucket, check, command, Context, cooldown
from bot.translations import EnUsDecorators, Response


@base_decorator(EnUsDecorators.Chance)
@cooldown(rate=3, per=10, bucket=Bucket.user)
@check([])
@command(name='chance', aliases=['%'])
async def command(ctx: Context) -> Response:
    return ctx.translations.Chance.random_percentage.format_response(ctx, random.random() * 100)
