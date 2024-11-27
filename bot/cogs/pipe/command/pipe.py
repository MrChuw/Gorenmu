# -*- coding: utf-8 -*-
import re

from bot.bot import Gorenmu
from bot.ext.commands import base_decorator, Bucket, check, command, Command, Context, cooldown
from bot.translations import BaseDecorators, Response


@base_decorator(BaseDecorators.Others.Pipe)
@cooldown(rate=3, per=10, bucket=Bucket.user)
@check([])
@command(name='pipe', aliases=[])
async def command(ctx: Context) -> Response:
    if ctx.user.language == ctx.bot.TranslationManager.languages[0]:
        url = f"{ctx.bot.config.BotConfig.site_url}{ctx.bot.TranslationManager.languages[0]}/commands/pipe.html"
    elif ctx.user.language == ctx.bot.TranslationManager.languages[1]:
        url = f"{ctx.bot.config.BotConfig.site_url}{ctx.bot.TranslationManager.languages[1]}/comandos/pipe.html"

    else:
        url = f"{ctx.bot.config.BotConfig.site_url}{ctx.bot.TranslationManager.languages[0]}/commands/pipe.html"
    return ctx.translations.Others.Pipe.response.format_response(ctx, url)

