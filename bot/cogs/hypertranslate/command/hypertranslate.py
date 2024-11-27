# -*- coding: utf-8 -*-
import asyncio
import random

from bot.apis import GoogleTranslator
from bot.apis.translate.constants import GOOGLE_LANGUAGES_TO_CODES as GOOGLE_LANGS
from bot.apis.translate.exceptions import TooManyRequests
from bot.bot import Gorenmu
from bot.ext.commands import base_decorator, Bucket, check, command, Command, Context, cooldown
from bot.translations import BaseDecorators, BaseTranslations, Response


@base_decorator(BaseDecorators.HyperTranslate)
@cooldown(rate=3, per=10, bucket=Bucket.user)
@check([])
@command(name='hypertranslate', aliases=['ht'])
async def command(ctx: Context, quantity: str = None, *, content: str = "") -> Response:
    translations = ctx.translations.HyperTranslate()
    session = ctx.bot.SessionsCaches.TranslateCachedSession.session
    if not quantity.isdigit():
        return translations.quantity_error.format_response(ctx, ctx.prefix, success=False)
    sleep = 0 if int(quantity) > 500 else 0.5
    runs = 0
    quantity = int(quantity)
    await ctx.simple_response(ctx, translations.starter_string)
    while True:
        try:
            if runs == quantity + 1:
                break
            await asyncio.sleep(sleep)
            target = (
                    BaseTranslations.HyperTranslate.lang if runs == quantity - 1 else translations.lang if runs == quantity else random.choice(
                        list(GOOGLE_LANGS.values())
                        ))
            translator = GoogleTranslator(session=session, target=target)
            content = await translator.translate(content)
            runs += 1
        except TooManyRequests as e:
            ctx.bot.log.warning(e)
            await asyncio.sleep(60)
        except Exception as e:
            ctx.bot.log.error(e)
            await asyncio.sleep(10)
    if not content:
        return translations.unexpected_error.format_response(ctx, success=False)
    return translations.translation.format_response(ctx, content)

