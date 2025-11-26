from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from aiohttp import ClientResponse
from aiohttp_client_cache import CachedSession
from bs4 import BeautifulSoup

from bot.ext import Context, Response, commands
from bot.utils import SessionsCaches

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class RandomSCPCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot)
        self.SessionsCaches: SessionsCaches = SessionsCaches(bot)

    cooldown_rate = 1
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: Context) -> bool:  # NOQA
        return True

    @commands.command(name="randomscp", aliases=["rscp"])
    async def randomscp(self, ctx: Context) -> Response:
        session = self.SessionsCaches.Scp.session
        start_time = asyncio.get_event_loop().time()
        try:
            while True:
                scp = await get_scp(session)
                if scp.status != 404:
                    break
                if asyncio.get_event_loop().time() - start_time >= 30:
                    return self.translations.Exceptions.timeout(ctx)
                await asyncio.sleep(1)

            return self.translations.Exceptions.echo(ctx, scp.url.human_repr())
        except Exception as e:
            ctx.bot.log.error(e, exc_info=e)
            return self.translations.Exceptions.unexpected_error(ctx, e)


async def get_scp(session: CachedSession) -> ClientResponse:
    async with session.disabled():
        response = await session.get("https://scp-wiki.wikidot.com/random:random-page")  # NOQA
    soup = BeautifulSoup(await response.text(), "html.parser")
    iframe = soup.find(
        "iframe",
        src=lambda x: x and "https://snippets.wdfiles.com/local--code/code:" in x,
    )
    url = iframe["src"].replace("https://snippets.wdfiles.com/local--code/code:iframe-redirect#http", "https")  # NOQA
    return await session.head(url)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(RandomSCPCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
