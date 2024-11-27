# -*- coding: utf-8 -*-
import asyncio

from aiohttp_client_cache import CachedResponse, CachedSession

from bot.bot import Gorenmu
from bot.ext.commands import base_decorator, Bucket, check, command, Command, Context, cooldown
from bot.translations import BaseDecorators, Response


async def get_wiki(session: CachedSession, url: str) -> CachedResponse:
    async with session.disabled():
        await asyncio.sleep(1)
        response = await session.get(url, allow_redirects=True)  # NOQA
    return response  # NOQA


@base_decorator(BaseDecorators.Wikihow)
@cooldown(rate=3, per=10, bucket=Bucket.user)
@check([])
@command(name='wikihow', aliases=[])
async def command(ctx: Context, *, quantity="") -> Response:
    translations = ctx.translations.Wikihow
    quantity = int(quantity) if quantity.isdigit() else 1
    quantity = min(quantity, 10) if ctx.author.name != "mr_chuw" else quantity
    session = ctx.bot.SessionsCaches.WikihowCachedSession.session
    responses = []
    try:
        for _ in range(quantity):
            wiki = await get_wiki(session, translations.url)
            while wiki.status == 404:
                wiki = await get_wiki(session, translations.url)
            if wiki.status in [200, 304]:
                responses.append(wiki.url.human_repr())
        return translations.links.format_response(ctx, response_list=responses)
    except Exception as e:
        ctx.bot.log.error(e, exc_info=e)
        return translations.unexpected_error.format_response(ctx, success=False)


