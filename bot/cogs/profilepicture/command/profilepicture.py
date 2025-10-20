# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Context, Response, commands
from bot.utils import SessionsCaches, StringTools, TimeTools, UploadThings

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class ProfilePictureCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot)
        self.StringTools: StringTools = StringTools()
        self.SessionsCaches: SessionsCaches = SessionsCaches(bot)
        self.UploadThings: UploadThings = UploadThings(bot)

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: commands.Context) -> bool:  # NOQA
        return True

    @commands.command(name="profilepicture", aliases=["pfp"])
    async def profilepicture(self, ctx: Context, name: str = "") -> Response:
        translations = self.translations
        name = self.StringTools.str2name_or(name or ctx.author.name)
        user_tmi = await ctx.bot.fetch_user(login=name)
        if not user_tmi:
            return translations.Exceptions.user_not_found_name(ctx, name)
        profile_url = user_tmi.profile_image.url.replace("300x300", "600x600")
        session = self.SessionsCaches.ProfilePicture.session
        image_tmi = await session.get(profile_url)
        imagem = await image_tmi.read()

        uploaded_image = await self.UploadThings.upload_file(
            data=imagem,
            mime_type="image/png",
            filename="profile_pic.png",
            session=session,
            url=self.bot.config.ApisConfig.feridinha_url,
            api_key={"token": self.bot.config.ApisConfig.feridinha_key},
        )
        uploaded_shorter = None
        if uploaded_image:
            uploaded_shorter = await self.UploadThings.shortener(
                uploaded_image, tags=["ProfilePicture"], session=session
            )
        profile_shorter = None
        if uploaded_shorter:
            profile_shorter = await self.UploadThings.shortener(profile_url, tags=["ProfilePicture"], session=session)
        response = ""
        if uploaded_image:
            response += f"{uploaded_image} "

        if profile_shorter:
            response += f"{profile_shorter} "
        else:
            response += f"{profile_url} " if type(profile_url) is str else ""

        return translations.Exceptions.echo(ctx, response)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(ProfilePictureCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
