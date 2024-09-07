# -*- coding: utf-8 -*-
import asyncio
import datetime
from bot.bot import Gorenmu
from bot.models import User, Channel
from bot.utils import Check, Role
from typing import Dict, Any, List, Tuple, Optional, Coroutine, Callable
from bot.ext.commands import Bucket, check, Context, cooldown, base_decorator, helper, usage, command
from bot.translations import EnTranslations, EnDecorators, Response
from bot.bot import Gorenmu
from bot.ext.commands import Command
import random
from bot.apis import Color


@base_decorator(EnDecorators.RandomColor)
@cooldown(rate=3, per=10, bucket=Bucket.user)
@check([])
@command(name="randomcolor", aliases=["rc"])
async def command(ctx: Context) -> Response:
    translations = ctx.translations.RandomColor
    hex_code = "%06x" % random.randint(0, 0xFFFFFF)
    url = ctx.bot.config.ApisConfig.hex_site_url + hex_code
    session = ctx.bot.SessionsCaches.ColorCachedSession.session
    return translations.response_url.format_response(ctx, hex_code, await Color.name(hex_code, session), url)



def dynamic_description(command_: Command, bot: Gorenmu, ctx: Context = None, ) -> dict[str, dict[str, str]]:
    responses: dict[str, dict[str, str]] = {}
    cooldown_ = command_._cooldowns[0]  # NOQA
    per = cooldown_._per  # NOQA
    rate = cooldown_._rate  # NOQA
    prefix = ctx.prefix if ctx else bot.config.BotConfig.prefix[0]
    for lang in command_.decorators:
        if lang not in responses:
            responses[lang] = {}
        decorator: EnDecorators.RandomColor = command_.decorators[lang]
        description = decorator.get_description(decorator)  # NOQA
        base_decorators = bot.TranslationManager.get_decorator(lang)
        cooldown_type = base_decorators.get_bucket_type(cooldown_.bucket)
        afk_template = getattr(decorator, 'template', EnDecorators.RandomColor.template).format(
                rate=rate,
                per=per,
                cooldown_type=cooldown_type,
                description=description,
                command_title=command_.name.capitalize(),
                command_name=command_.name.lower(),
                prefix=prefix,
                aliases=", ".join(command_.aliases)
                )

        responses[lang][command_.name.lower()] = afk_template





    return responses










