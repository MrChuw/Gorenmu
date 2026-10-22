from __future__ import annotations

import asyncio
import re
from typing import TYPE_CHECKING

from aiohttp import ClientResponse
from aiohttp_client_cache import CachedSession
from bs4 import BeautifulSoup, Tag

from bot.ext import Context, Response, commands
from bot.utils import SessionsCaches

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class RandomSCPCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot, self)
        self.SessionsCaches: SessionsCaches = SessionsCaches(bot)


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

            return self.translations.Exceptions.echo(scp.url.human_repr())
        except Exception as e:
            ctx.bot.log.warning(e, exc_info=e)
            await ctx.bot.CommandHandler.send_bug(ctx, e, ping=False)
            return self.translations.Exceptions.error()


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(RandomSCPCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA


class SCPNotFoundError(Exception):
    pass


IFRAME_SRC_PATTERN = re.compile(r"^https://snippets\.wdfiles\.com/local--code/code:")


async def get_scp(session: CachedSession) -> ClientResponse:
    async with session.disabled():
        response = await session.get("https://scp-wiki.wikidot.com/random:random-page")

    soup = BeautifulSoup(await response.text(), "html.parser")
    iframe = soup.find("iframe", src=IFRAME_SRC_PATTERN)


    if not isinstance(iframe, Tag):
        raise SCPNotFoundError("Could not find a valid redirect iframe tag.")

    src = iframe.get("src")
    if not src or not isinstance(src, str):
        raise SCPNotFoundError("Redirect iframe is missing a valid 'src' attribute.")

    url = src.replace("https://snippets.wdfiles.com/local--code/code:iframe-redirect#http", "https")
    return await session.head(url)

