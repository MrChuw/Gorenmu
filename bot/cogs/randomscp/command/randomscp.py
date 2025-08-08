# -*- coding: utf-8 -*-
from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from aiohttp_client_cache import CachedSession, response
from bs4 import BeautifulSoup

from bot.ext import Context, commands
from bot.translations import Response

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class RandomSCPCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot

    cooldown_rate = 1
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: Context) -> bool:  # NOQA
        return True

    @commands.base_decorator("Scp")
    @commands.command(name="randomscp", aliases=["rscp"])
    async def randomscp(self, ctx: Context) -> Response:
        session = ctx.bot.SessionsCaches.ScpCachedSession.session
        start_time = asyncio.get_event_loop().time()
        try:
            while True:
                scp = await get_scp(session)
                if scp.status != 404:
                    break
                if asyncio.get_event_loop().time() - start_time >= 30:
                    return ctx.user.translations.Exceptions.timeout.format_response(ctx)
                await asyncio.sleep(1)

            return ctx.user.translations.Exceptions.link.format_response(ctx, scp.url.human_repr())
        except Exception as e:
            ctx.bot.log.error(e, exc_info=e)
            return ctx.user.translations.Exceptions.unexpected_error.format_response(ctx, success=False)


async def get_scp(session: CachedSession) -> response:
    async with session.disabled():
        response = await session.get("https://scp-wiki.wikidot.com/random:random-page")  # NOQA
    soup = BeautifulSoup(await response.text(), "html.parser")
    iframe = soup.find("iframe", src=lambda x: x and "https://snippets.wdfiles.com/local--code/code:" in x)
    url = iframe["src"].replace("https://snippets.wdfiles.com/local--code/code:iframe-redirect#http", "https")  # NOQA
    return await session.head(url)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(RandomSCPCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
