# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import TYPE_CHECKING

from bot.ext import commands, Context
from bot.translations import BaseDecorators, Response
import asyncio

if TYPE_CHECKING:
    from bot.bot import Gorenmu

__all__ = (
        'PlaceHolderCmd'
)

BaseDeco = BaseDecorators


class PlaceHolderCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None:
        ...

    @commands.Component.guard()
    def guards_component(self, ctx: commands.Context) -> bool:
        return True

    @commands.base_decorator(BaseDeco)
    @commands.command(name='PlaceHolder', aliases=[])
    async def PlaceHolder(self, ctx: Context) -> Response:
        translations = ctx.user.translations.Wikipedia
        session = ctx.bot.SessionsCaches.WikipediaCachedSession.session
        responses = []
        try:
            wiki = await ctx.bot.SessionsCaches.WikihowCachedSession.get_not_cached(session, translations.url)
            while wiki.status == 404:
                wiki = await ctx.bot.SessionsCaches.WikihowCachedSession.get_not_cached(session, translations.url)
                await asyncio.sleep(2)
            if wiki.status == 200:
                responses.append(wiki.url.human_repr())
            return translations.links.format_response(ctx, response_list=responses)
        except Exception as e:
            ctx.bot.log.error(e, exc_info=e)
            return ctx.user.translations.Exceptions.unexpected_error.format_response(ctx, success=False)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(PlaceHolderCmd(bot))


async def teardown(bot: Gorenmu) -> None:
    ...
