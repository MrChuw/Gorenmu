# -*- coding: utf-8 -*-
import asyncio
import random

from bot.apis import GoogleTranslator
from bot.apis.translate.constants import GOOGLE_LANGUAGES_TO_CODES as GOOGLE_LANGS
from bot.apis.translate.exceptions import TooManyRequests
from bot.bot import Gorenmu
from bot.ext.commands import base_decorator, Bucket, check, command, Command, Context, cooldown
from bot.translations import EnDecorators, Response


@base_decorator(EnDecorators.HyperTranslate)
@cooldown(rate=3, per=10, bucket=Bucket.user)
@check([])
@command(name='hypertranslate', aliases=['ht'])
async def command(ctx: Context, quantidade: str = None, *, content: str = "") -> Response:
    translations = ctx.translations.HyperTranslate()
    session = ctx.bot.SessionsCaches.TranslateCachedSession.session
    if quantidade.isdigit() is False:
        return translations.quantity_error.format_response(ctx, ctx.prefix, success=False)
    sleep = 0 if int(quantidade) > 500 else 0.5
    runs = 0
    quantidade = int(quantidade)
    await ctx.simple_response(ctx, translations.starter_string)
    while True:
        try:
            if runs == quantidade + 1:
                break
            await asyncio.sleep(sleep)
            target = translations.lang if runs == quantidade else random.choice(list(GOOGLE_LANGS.values()))
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


def dynamic_description(command_: Command, bot: Gorenmu, ctx: Context = None, ) -> dict[str, dict[str, str]]:
    responses: dict[str, dict[str, str]] = {}
    cooldown_ = command_._cooldowns[0]  # NOQA
    per = cooldown_._per  # NOQA
    rate = cooldown_._rate  # NOQA
    prefix = ctx.prefix if ctx else bot.config.BotConfig.prefix[0]
    for lang in command_.decorators:
        if lang not in responses:
            responses[lang] = {}
        decorator: EnDecorators.HyperTranslate = command_.decorators[lang]
        description = decorator.get_description(decorator)  # NOQA
        base_decorators = bot.TranslationManager.get_decorator(lang)
        cooldown_type = base_decorators.get_bucket_type(cooldown_.bucket)
        afk_template = getattr(decorator, 'template', EnDecorators.HyperTranslate.template).format(rate=rate, per=per,
                cooldown_type=cooldown_type, description=description, command_title=command_.name.capitalize(),
                command_name=command_.name.lower(), prefix=prefix, aliases=", ".join(command_.aliases)
        )
        responses[lang][command_.name.lower()] = afk_template
    return responses
