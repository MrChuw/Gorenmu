# -*- coding: utf-8 -*-
from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from bot.ext import Context, commands
from bot.translations import Response
from bot.utils import SessionsCaches

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


# TODO: add Special:RandomInCategory/CategoryName


class WikipediaCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot)
        self.SessionsCaches: SessionsCaches = SessionsCaches(bot)

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: Context) -> bool:  # NOQA
        return True

    @commands.command(name="wikipedia", aliases=[])
    async def wikipedia(self, ctx: Context) -> Response:
        url = self.translations.Wikipedia.url(ctx)
        session = self.SessionsCaches.WikipediaCachedSession.session
        start_time = asyncio.get_event_loop().time()
        try:
            while True:
                wiki = await self.SessionsCaches.WikipediaCachedSession.get_not_cached(session, url)
                if wiki.status != 404:
                    break
                if asyncio.get_event_loop().time() - start_time >= 30:
                    return self.translations.Exceptions.timeout(ctx)
                await asyncio.sleep(1)

            return self.translations.Exceptions.echo(ctx, wiki.url.human_repr())
        except Exception as e:
            ctx.bot.log.error(e, exc_info=e)
            return self.translations.Exceptions.unexpected_error(ctx, e)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(WikipediaCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
