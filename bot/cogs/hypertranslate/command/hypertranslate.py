from __future__ import annotations

import asyncio
import random
from typing import TYPE_CHECKING

from bot.apis import GoogleTranslator
from bot.apis.translate.constants import GOOGLE_LANGUAGES_TO_CODES as GOOGLE_LANGS
from bot.apis.translate.exceptions import TooManyRequests
from bot.ext import Context, Response, commands
from bot.utils import SessionsCaches, StringTools

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class HyperTranslateCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot, self)
        self.SessionsCaches: SessionsCaches = SessionsCaches(bot)
        self.StringTools: StringTools = StringTools()

    @commands.command(name="hypertranslate", aliases=["ht"])  # TODO: add reply_to
    async def hypertranslate(self, ctx: Context, quantity_in: str, *, text_in: str = "") -> Response:
        translations = self.translations.HyperTranslate
        session = self.SessionsCaches.Translate.session
        if not quantity_in.isdigit():
            text = f"{quantity_in} {text_in}".replace("  ", " ")
            quantity = 10
        else:
            text = text_in
            quantity = int(quantity_in)
        text, output_lang = self.StringTools.remove_prefixed_option(text, "lang:")
        sleep = 0 if quantity > 500 else 0.5
        await ctx.simple_response(ctx, translations.starter_string())
        for runs in range(1, quantity + 2):
            try:
                await asyncio.sleep(sleep)
                if runs == quantity:
                    target = "en"
                elif runs == quantity + 1:
                    target = output_lang or translations.base_lang()
                else:
                    target = random.choice(list(GOOGLE_LANGS.values()))
                translator = GoogleTranslator(session=session, target=target)
                text = await translator.translate(text)
            except TooManyRequests as e:
                ctx.bot.log.warning(e)
                await asyncio.sleep(60)
            except Exception as e:
                ctx.bot.log.error(e)
                await asyncio.sleep(10)

        if not text:
            return translations.unexpected_error()
        return translations.translation(text)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(HyperTranslateCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
