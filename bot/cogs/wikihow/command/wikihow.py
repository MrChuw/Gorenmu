# -*- coding: utf-8 -*-
from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from bot.ext import commands, Context
from bot.translations import BaseDecorators, Response

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class WikiHowCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: commands.Context) -> bool:  # NOQA
        return True

    @commands.base_decorator(BaseDecorators.Wikihow)
    @commands.command(name="wikihow", aliases=[])
    async def wikihow(self, ctx: Context) -> Response:
        translations = ctx.user.translations.Wikihow
        session = ctx.bot.SessionsCaches.WikihowCachedSession.session
        start_time = asyncio.get_event_loop().time()
        try:
            while True:
                wiki = await ctx.bot.SessionsCaches.WikihowCachedSession.get_not_cached(session, translations.url)
                if wiki.status in [200, 304]:
                    break
                if asyncio.get_event_loop().time() - start_time >= 30:
                    return ctx.user.translations.Wikihow.timeout.format_response(ctx)
                await asyncio.sleep(1)

            return translations.links.format_response(ctx, wiki.url.human_repr())
        except Exception as e:
            ctx.bot.log.error(e, exc_info=e)
            return ctx.user.translations.Exceptions.unexpected_error.format_response(ctx, success=False)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(WikiHowCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
