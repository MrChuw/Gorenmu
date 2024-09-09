# -*- coding: utf-8 -*-
import asyncio

from aiohttp_client_cache import CachedSession, CachedResponse

from bot.bot import Gorenmu
from bot.ext.commands import base_decorator, Bucket, check, command, Command, Context, cooldown
from bot.translations import EnDecorators, Response
from loguru import logger


async def get_wiki(session: CachedSession, url: str) -> CachedResponse:
    await asyncio.sleep(2)
    async with session.disabled():
        response = await session.get(url, allow_redirects=True)  # NOQA
    return response  # NOQA



@base_decorator(EnDecorators.Wikipedia)
@cooldown(rate=3, per=10, bucket=Bucket.user)
@check([])
@command(name='wikipedia', aliases=[''])
async def command(ctx: Context) -> Response:
    translations = ctx.translations.Wikipedia
    session = ctx.bot.SessionsCaches.WikipediaCachedSession.session
    responses = []
    try:
        wiki = await get_wiki(session, translations.url)
        while wiki.status == 404:
            wiki = await get_wiki(session, translations.url)
            await asyncio.sleep(2)
        if wiki.status == 200:
            responses.append(wiki.url.human_repr())
        return translations.links.format_response(ctx, response_list=responses)
    except Exception as e:
        ctx.bot.log.error(e, exc_info=e)
        return translations.unexpected_error.format_response(ctx, success=False)



def dynamic_description(command_: Command, bot: Gorenmu, ctx: Context = None, ) -> dict[str, dict[str, str]]:
    responses: dict[str, dict[str, str]] = {}
    cooldown_ = command_._cooldowns[0]  # NOQA
    per = cooldown_._per  # NOQA
    rate = cooldown_._rate  # NOQA
    prefix = ctx.prefix if ctx else bot.config.BotConfig.prefix[0]
    for lang in command_.decorators:
        if lang not in responses:
            responses[lang] = {}
        decorator: EnDecorators.Wikipedia = command_.decorators[lang]
        description = decorator.get_description(decorator)  # NOQA
        base_decorators = bot.TranslationManager.get_decorator(lang)
        cooldown_type = base_decorators.get_bucket_type(cooldown_.bucket)
        afk_template = getattr(decorator, 'template', EnDecorators.Wikipedia.template).format(
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










