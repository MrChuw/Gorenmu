# -*- coding: utf-8 -*-
import random
import re

from bot.bot import Gorenmu
from bot.ext.commands import base_decorator, Bucket, check, command, Command, Context, cooldown
from bot.translations import BaseDecorators, Response


@base_decorator(BaseDecorators.Choice)
@cooldown(rate=3, per=10, bucket=Bucket.user)
@check([])
@command(name='choice', aliases=['pick'])
async def command(ctx: Context, *, content: str) -> Response:
    pattern = '|'.join(map(re.escape, ctx.translations.Choice.choice_separators))
    choice = random.choice([arg for arg in re.split(pattern, content) if arg])
    return ctx.translations.Choice.chosen_option.format_response(ctx, choice)


