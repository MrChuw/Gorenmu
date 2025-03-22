# -*- coding: utf-8 -*-
from __future__ import annotations

import asyncio
import random
from typing import TYPE_CHECKING

from bot.apis import GoogleTranslator
from bot.apis.translate.constants import GOOGLE_LANGUAGES_TO_CODES as GOOGLE_LANGS
from bot.apis.translate.exceptions import TooManyRequests
from bot.ext import commands, Context
from bot.translations import BaseDecorators, Response

if TYPE_CHECKING:
    from bot.bot import Gorenmu

__all__ = 'HyperTranslateCmd'


class HyperTranslateCmd(commands.CustomComponent):
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

    @commands.base_decorator(BaseDecorators.HyperTranslate)
    @commands.command(name='hypertranslate', aliases=['ht'])
    async def hypertranslate(self, ctx: Context, quantity: str = 10, *, text: str = "") -> Response:
        translations = ctx.user.translations.HyperTranslate
        session = ctx.bot.SessionsCaches.TranslateCachedSession.session
        if not quantity.isdigit():
            text = f"{quantity} {text}".replace("  ", " ")
            quantity = 10
        quantity = int(quantity)
        text, output_lang = ctx.bot.ToolsTools.remove_prefixed_option(text, "lang:")
        sleep = 0 if quantity > 500 else 0.5
        runs = 0
        await ctx.simple_response(ctx, translations.starter_string)
        while True:
            try:
                if runs == quantity + 1:
                    break
                await asyncio.sleep(sleep)
                if runs == quantity - 1:
                    target = "en"
                elif runs == quantity:
                    target = output_lang or translations.lang
                else:
                    target = random.choice(list(GOOGLE_LANGS.values()))
                translator = GoogleTranslator(session=session, target=target)
                text = await translator.translate(text)
                runs += 1
            except TooManyRequests as e:
                ctx.bot.log.warning(e)
                await asyncio.sleep(60)
            except Exception as e:
                ctx.bot.log.error(e)
                await asyncio.sleep(10)
        if not text:
            return translations.unexpected_error.format_response(ctx, success=False)
        return translations.translation.format_response(ctx, text)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(HyperTranslateCmd(bot))


async def teardown(bot: Gorenmu) -> None:
    ...
