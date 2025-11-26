from __future__ import annotations

import asyncio
from random import randint
from typing import TYPE_CHECKING

from yarl import URL

from bot.apis import booru
from bot.ext import Context, Response, commands
from bot.utils import SessionsCaches, TimeTools, UploadThings

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class SafeBooruCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot)
        self.TimeTools: TimeTools = TimeTools()
        self.SessionsCaches: SessionsCaches = SessionsCaches(bot)
        self.UploadThings: UploadThings = UploadThings(bot)

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: Context) -> bool:  # NOQA
        return True

    @commands.command(name="safebooru", aliases=[])
    async def safebooru(self, ctx: Context, *, args: str = "") -> Response:
        translations = self.translations.Safebooru
        tags = args.split(" ")

        if len(tags) > 10:
            return translations.too_much_tags(ctx, 10)
        timeout = self.TimeTools.Timeout(15)

        while True:
            _img, img_preview, response_final = await response(ctx, " ".join(tags), timeout, self)
            if not img_preview:
                return self.translations.Exceptions.unexpected_error(ctx, response_final)
            if response_final:
                return translations.success(ctx, response_final)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(SafeBooruCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA


async def response(ctx: Context, args: str, timeout, command: SafeBooruCmd):
    img, img_preview = await choices(args, timeout, ctx, command)
    if img_preview == "error":
        return None, False, img

    translation = command.translations.Safebooru
    if not img or not img_preview:
        return None, None, False

    response_final = " ".join(
        (
            f"{translation.original(ctx)}: {img[i]} || {translation.preview(ctx)}: {img_preview[i]}"
            if img_preview[i]
            else f"{translation.original(ctx)}: {img[i]}"
        )
        for i in range(len(img))
    )
    return img, img_preview, response_final or False


async def choices(args: str, timeout: TimeTools.Timeout, ctx: Context, command: SafeBooruCmd):
    session = command.SessionsCaches.Safebooru.session
    instance = booru.Booru().Safebooru(session=session)
    while timeout.still_valid():
        try:
            await asyncio.sleep(0.2)
            image, preview = await instance.random(query=args, page=randint(0, 100))
            return await shortener(image, preview, ctx, command)
        except Exception as e:
            ctx.bot.log.error(e)
    return (
        command.translations.SupportTools.TimeTools.Humanize.precisedelta(timeout.elapsed()),
        "error",
    )


async def shortener(images: list[URL], images_preview: list[URL], ctx: Context, command: SafeBooruCmd):
    session = command.SessionsCaches.Safebooru.session
    shortener_ = command.UploadThings.shortener

    async def shorten(imagem):
        return await shortener_(imagem.human_repr() if imagem else None, ["booru"], session)

    return (
        [await shorten(imagem) for imagem in images],
        [await shorten(imagem_preview) for imagem_preview in images_preview],
    )
