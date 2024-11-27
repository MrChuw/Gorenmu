# -*- coding: utf-8 -*-
import random

from bot.apis import Color
from bot.bot import Gorenmu
from bot.ext.commands import base_decorator, Bucket, check, command, Command, Context, cooldown
from bot.translations import BaseDecorators, Response


@base_decorator(BaseDecorators.RandomColor)
@cooldown(rate=3, per=10, bucket=Bucket.user)
@check([])
@command(name="randomcolor", aliases=["rc"])
async def command(ctx: Context) -> Response:
    translations = ctx.translations.RandomColor
    hex_code = "%06x" % random.randint(0, 0xFFFFFF)
    url = ctx.bot.config.ApisConfig.hex_site_url + hex_code
    session = ctx.bot.SessionsCaches.ColorCachedSession.session
    return translations.response_url.format_response(ctx, hex_code, await Color.name(hex_code, session), url)


