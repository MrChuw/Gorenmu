from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from bot.ext import Context, Response, commands
from bot.utils import SessionsCaches, StringTools

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


# TODO: add Special:RandomInCategory/CategoryName


class WikipediaCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot, self)
        self.StringTools: StringTools = StringTools()
        self.SessionsCaches: SessionsCaches = SessionsCaches(bot)

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    async def component_before_invoke(self, ctx: Context) -> None:
        self.translations.ctx_set(ctx)

    @commands.Component.guard()
    def guards_component(self, ctx: Context) -> bool:  # NOQA
        return True

    @commands.command(name="wikipedia", aliases=[])
    async def wikipedia(self, ctx: Context, lang="") -> Response:
        _, lang = self.StringTools.extract_and_remove_field(lang, "lang", ctx.user.language or "en")
        url = self.translations.Wikipedia.url(lang)
        session = self.SessionsCaches.Wikipedia.session
        start_time = asyncio.get_event_loop().time()
        try:
            while True:
                wiki = await self.SessionsCaches.Wikipedia.get_not_cached(session, url)
                if wiki.status != 404:
                    break
                if asyncio.get_event_loop().time() - start_time >= 30:
                    return self.translations.Exceptions.timeout(ctx)
                await asyncio.sleep(1)

            return self.translations.Exceptions.echo(wiki.url.human_repr())
        except Exception as e:
            ctx.bot.log.warning(e, exc_info=e)
            await ctx.bot.CommandHandler.send_bug(ctx, e, ping=False)
            return self.translations.Exceptions.error(ctx)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(WikipediaCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
