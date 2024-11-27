# -*- coding: utf-8 -*-
import asyncio

from aiohttp_client_cache import CachedSession, response
from bs4 import BeautifulSoup

from bot.bot import Gorenmu
from bot.ext.commands import base_decorator, Bucket, check, command, Command, Context, cooldown
from bot.translations import BaseDecorators, Response


async def get_scp(session: CachedSession) -> response:
    async with session.disabled():
        response = await session.get("https://scp-wiki.wikidot.com/random:random-page")  # NOQA
    soup = BeautifulSoup(await response.text(), 'html.parser')
    iframe = soup.find('iframe', src=lambda x: x and 'https://snippets.wdfiles.com/local--code/code:' in x)
    url = iframe['src'].replace("https://snippets.wdfiles.com/local--code/code:iframe-redirect#http", "https")  # NOQA
    return await session.head(url)


@base_decorator(BaseDecorators.Scp)
@cooldown(rate=3, per=10, bucket=Bucket.user)
@check([])
@command(name='randomscp', aliases=['rscp'])
async def command(ctx: Context, quantity: str = "") -> Response:
    translations = ctx.translations.Scp
    quantity = int(quantity) if quantity.isdigit() else 1
    quantity = min(quantity, 10) if ctx.author.name != "mr_chuw" else quantity
    session = ctx.bot.SessionsCaches.ScpCachedSession.session
    responses = []
    try:
        for _ in range(quantity):
            scp = await get_scp(session)
            while scp.status == 404:
                scp = await get_scp(session)
                await asyncio.sleep(1)
            if scp.status == 200:
                responses.append(scp.url.human_repr())
        return translations.links.format_response(ctx, response_list=responses)
    except Exception as e:
        ctx.bot.log.error(e, exc_info=e)
        return translations.unexpected_error.format_response(ctx, success=False)
