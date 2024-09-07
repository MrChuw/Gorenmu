# -*- coding: utf-8 -*-
import asyncio
import datetime
from bot.bot import Gorenmu
from bot.models import User, Channel, Imgur
from bot.utils import Check, Role
from typing import Dict, Any, List, Tuple, Optional, Coroutine, Callable
from bot.ext.commands import Bucket, check, Context, cooldown, base_decorator, helper, usage, command, Command
from bot.translations import EnTranslations, EnDecorators, Response
from typing import AsyncIterator
from collections import defaultdict

@base_decorator(EnDecorators.NSFW.ImgurRepeated)
@cooldown(rate=3, per=10, bucket=Bucket.mod)
@check([])
@command(name='imgur_repeated', aliases=[''])
async def command(ctx: Context) -> Response:
    translations = ctx.translations.NSFW.ImgurRepeated
    urls: dict[str, int] = {}
    async for links in get_links():
        urls = defaultdict(int)
        for link in links:
            urls[link.link] += 1
    sorted_urls = {k: v for k, v in sorted(urls.items(), key=lambda x: x[1], reverse=True) if v > 1}
    if not sorted_urls:
        return translations.no_repeated.format_response(ctx)
    duplicates = [f"https://i.imgur.com/{link}.jpg" for link in sorted_urls]
    embed = await ctx.bot.UploadThings.send_imgur(duplicates, ctx.bot, ctx.bot.SessionsCaches.ImgurCachedSession.session)
    return translations.links_repeated.format_response(ctx, len(duplicates), embed)


async def get_links() -> AsyncIterator[list[Imgur]]:
    offset = 0
    batch_size = 100
    while True:
        items = await Imgur.all().offset(offset).limit(batch_size)

        if not items:
            break

        yield items
        offset += batch_size



def dynamic_description(command_: Command, bot: Gorenmu, ctx: Context = None, ) -> dict[str, dict[str, str]]:
    responses: dict[str, dict[str, str]] = {}
    cooldown_ = command_._cooldowns[0]  # NOQA
    per = cooldown_._per  # NOQA
    rate = cooldown_._rate  # NOQA
    prefix = ctx.prefix if ctx else bot.config.BotConfig.prefix[0]
    for lang in command_.decorators:
        if lang not in responses:
            responses[lang] = {}
        decorator: EnDecorators.NSFW.ImgurRepeated = command_.decorators[lang]
        description = decorator.get_description(decorator)  # NOQA
        base_decorators = bot.TranslationManager.get_decorator(lang)
        cooldown_type = base_decorators.get_bucket_type(cooldown_.bucket)
        afk_template = getattr(decorator, 'template', EnDecorators.NSFW.ImgurRepeated.template).format(
                rate=rate,
                per=per,
                cooldown_type=cooldown_type,
                description=description,
                command_title=command_.name.capitalize(),
                command_name=command_.name.lower(),
                prefix=prefix,
        )

        responses[lang][command_.name.lower()] = afk_template

    return responses
