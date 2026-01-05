from __future__ import annotations

import asyncio
import inspect
import types
from typing import TYPE_CHECKING

from urlextract import URLExtract

from bot.ext import Context, Response, commands
from bot.utils import SessionsCaches, UploadThings

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class ShortenCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot)
        self.UploadThings: UploadThings = UploadThings(bot)
        self.SessionsCaches: SessionsCaches = SessionsCaches(bot)

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: commands.Context) -> bool:  # NOQA
        return True

    async def component_before_invoke(self, ctx: Context) -> None:
        self.translations.ctx_set(ctx)

    # TODO: Fix crash on no-https on url(s)
    @commands.command(name="shorten", aliases=["short"])
    async def shorten(self, ctx: Context, *, content) -> Response:
        links = URLExtract().find_urls(text=content)
        if not links:
            ...
        session = self.SessionsCaches.Shorten.session
        if len(links) > 1:
            link = ""
            for url in links:
                await asyncio.sleep(0.1)
                short = await self.UploadThings.shortener(url, ["shortener"], session)
                if not short:
                    fake_exc = fake_stacktrace(f"External shortener API failed for: {url}")
                    await self.bot.CommandHandler.send_bug(ctx, fake_exc)
                    return self.translations.Shorten.api_erro()
                link += f"{short} "
            return self.translations.Shorten.urls(link)
        else:
            short = await self.UploadThings.shortener(links[0], ["shortener"], session)
            if short:
                return self.translations.Shorten.url(short)
            fake_exc = fake_stacktrace(f"External shortener API failed for: {links[0]}")
            await self.bot.CommandHandler.send_bug(ctx, fake_exc)
            return self.translations.Shorten.api_erro()


def fake_stacktrace(message: str) -> Exception | None:
    exc = Exception(message)
    tb = types.TracebackType(tb_next=None, tb_frame=inspect.currentframe().f_back, tb_lasti=0, tb_lineno=1)

    exc.__traceback__ = tb
    return exc


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(ShortenCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
