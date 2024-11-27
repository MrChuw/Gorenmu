# -*- coding: utf-8 -*-
import random

from bot.bot import Gorenmu
from bot.ext.commands import base_decorator, Bucket, check, command, Command, Context, cooldown
from bot.translations import BaseDecorators, Response


@base_decorator(BaseDecorators.Chance)
@cooldown(rate=3, per=10, bucket=Bucket.user)
@check([])
@command(name='chance', aliases=['%'])
async def command(ctx: Context) -> Response:
    return ctx.translations.Chance.random_percentage.format_response(ctx, random.random() * 100)


