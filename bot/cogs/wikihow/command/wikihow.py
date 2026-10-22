from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from bot.ext import Context, Response, commands
from bot.utils import SessionsCaches, StringTools

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class WikiHowCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot, self)
        self.StringTools: StringTools = StringTools()
        self.SessionsCaches: SessionsCaches = SessionsCaches(bot)

    @commands.command(name="wikihow", aliases=[])
    async def wikihow(self, ctx: Context, lang="") -> Response:
        _, lang = self.StringTools.extract_and_remove_field(lang, "lang", ctx.user.language or "en")
        url = self.translations.Wikihow.url(lang)
        session = self.SessionsCaches.Wikihow.session
        start_time = asyncio.get_event_loop().time()
        try:
            while True:
                wiki = await self.SessionsCaches.Wikihow.get_not_cached(session, url)
                if wiki.status in [200, 304]:
                    break
                if asyncio.get_event_loop().time() - start_time >= 30:
                    return self.translations.Exceptions.timeout(ctx)
                await asyncio.sleep(1)

            return self.translations.Exceptions.echo(wiki.url.human_repr())
        except Exception as e:
            ctx.bot.log.warning(e, exc_info=e)
            await ctx.bot.CommandHandler.send_bug(ctx, e, ping=False)
            return self.translations.Exceptions.error()


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(WikiHowCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA


# TODO: test if works right the way is now, then other wise use this method.
"""
@helper('Envia um link do wikihow aleatório.')
@usage('para usar: <prefixo>wikihow <quantidade>')
@cooldown(rate=3, per=10, bucket=Bucket.user)
@command(aliases=[])
async def wikihow(self, ctx: Context, repete: str = "") -> None:
    repete = int(repete) if repete.isdigit() else 1
    repete = min(repete, 10) if ctx.author.name != 'mr_chuw' else repete

    try:
        # Usa o AsyncSession emulando o TLS do Chrome para contornar o WAF
        async with AsyncSession(impersonate="chrome150") as s:
            for _ in range(repete):
                r = await s.get("https://pt.wikihow.com/Special:Randomizer")
                url_formatada = unquote(r.url)

                await ctx.resposta(ctx, url_formatada)

                if repete > 1:
                    await asyncio.sleep(1.2)

    except Exception as e:
        return await ctx.resposta(ctx, "aconteceu algum erro, tente novamente.")
"""
