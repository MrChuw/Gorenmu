# -*- coding: utf-8 -*-
from __future__ import annotations

import asyncio
from random import randint
from typing import TYPE_CHECKING

from yarl import URL

from bot.apis import booru
from bot.ext import Context, commands
from bot.translations import Response

if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.utils import TimeTools


class SafeBooruCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: Context) -> bool:  # NOQA
        return True

    @commands.base_decorator("Safebooru")
    @commands.command(name="safebooru", aliases=[])
    async def safebooru(self, ctx: Context, *, args: str = "") -> Response:
        translations = ctx.user.translations.Safebooru
        tags = args.split(" ")

        if len(tags) > 10:
            return translations.too_much_tags.format_response(ctx, 10, success=False)
        timeout = ctx.bot.TimeTools.Timeout(15)

        while True:
            img, img_preview, response_final = await response(ctx, " ".join(tags), timeout)
            if not img_preview:
                return translations.unexpected_error.format_response(ctx, response_final, success=False)
            if response_final:
                return translations.success.format_response(ctx, response_final)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(SafeBooruCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA


async def response(ctx: Context, args: str, timeout):
    img, img_preview = await choices(args, timeout, ctx)
    if img_preview == "error":
        return None, False, img

    translation = ctx.user.translations.Safebooru
    if not img or not img_preview:
        return None, None, False

    response_final = " ".join(
        (
            f"{translation.original}: {img[i]} || {translation.preview}: {img_preview[i]}"
            if img_preview[i]
            else f"{translation.original}: {img[i]}"
        )
        for i in range(len(img))
    )
    return img, img_preview, response_final or False


async def choices(args: str, timeout: TimeTools.Timeout, ctx: Context):
    session = ctx.bot.SessionsCaches.SafebooruCachedSession.session
    instance = booru.Booru().Safebooru(session=session)
    while timeout.still_valid():
        try:
            await asyncio.sleep(0.2)
            image, preview = await instance.random(query=args, page=randint(0, 100))
            return await shortener(image, preview, ctx)
        except Exception as e:
            ctx.bot.log.error(e)
    return ctx.user.translations.SupportTools.TimeTools.Humanize.precisedelta(timeout.elapsed()), "error"


async def shortener(images: list[URL], images_preview: list[URL], ctx: Context):
    session = ctx.bot.SessionsCaches.SafebooruCachedSession.session
    shortener_ = ctx.bot.UploadThings.shortener

    async def shorten(imagem):
        return await shortener_(imagem.human_repr() if imagem else None, ["booru"], session)

    return (
        [await shorten(imagem) for imagem in images],
        [await shorten(imagem_preview) for imagem_preview in images_preview],
    )
