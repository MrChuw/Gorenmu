# -*- coding: utf-8 -*-
from __future__ import annotations

import re
import string
from typing import TYPE_CHECKING

from urlextract import URLExtract

from bot.ext import Context, Response, commands
from bot.utils import SessionsCaches

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class CountCmd(commands.CustomComponent):
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

    @commands.command(name="count", aliases=[])
    async def count(self, ctx: Context, *, content: str) -> Response:
        if (urls := URLExtract().find_urls(text=content)) and "type:url" in content:
            content = ""
            cache_session = self.SessionsCaches.CountCachedSession
            for url in urls:
                response = await cache_session.session.get(url)
                content += f"{await response.text()} "
        uppercase_count = len(re.findall(r"[A-Z]", content))
        punctuations_count = len(re.findall(f"[{re.escape(string.punctuation)}]", content))
        special_chars_count = len([char for char in re.findall(r"[^\w\s]", content) if char not in string.punctuation])
        return self.translations.Count.character_count(
            ctx, len(content), punctuations_count, uppercase_count, special_chars_count
        )


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(CountCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
