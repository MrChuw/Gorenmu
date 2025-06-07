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


class HyperTranslateCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: Context) -> bool:  # NOQA
        return True

    @commands.base_decorator(BaseDecorators.HyperTranslate)  # TODO: add reply_to
    @commands.command(name="hypertranslate", aliases=["ht"])
    async def hypertranslate(self, ctx: Context, quantity: str, *, text: str = "") -> Response:
        translations = ctx.user.translations.HyperTranslate
        session = ctx.bot.SessionsCaches.TranslateCachedSession.session
        if not quantity.isdigit():
            text = f"{quantity} {text}".replace("  ", " ")
            quantity = 10
        quantity = int(quantity)
        text, output_lang = ctx.bot.StringTools.remove_prefixed_option(text, "lang:")
        sleep = 0 if quantity > 500 else 0.5
        await ctx.simple_response(ctx, translations.starter_string)
        for runs in range(1, quantity + 2):
            try:
                await asyncio.sleep(sleep)
                if runs == quantity:
                    target = "en"
                elif runs == quantity + 1:
                    target = output_lang or translations.base_lang
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
            return translations.unexpected_error.format_response(ctx, success=False)
        return translations.translation.format_response(ctx, text)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(HyperTranslateCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
