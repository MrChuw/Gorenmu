# -*- coding: utf-8 -*-
import asyncio

from aiohttp_client_cache import CachedResponse, CachedSession

from bot.bot import Gorenmu
from bot.ext.commands import base_decorator, Bucket, check, command, Command, Context, cooldown
from bot.translations import BaseDecorators, Response


async def get_wiki(session: CachedSession, url: str) -> CachedResponse:
    await asyncio.sleep(2)
    async with session.disabled():
        response = await session.get(url, allow_redirects=True)  # NOQA
    return response  # NOQA


@base_decorator(BaseDecorators.Wikipedia)
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


