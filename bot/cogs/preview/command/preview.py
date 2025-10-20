# -*- coding: utf-8 -*-
from __future__ import annotations

import asyncio
import datetime
from typing import TYPE_CHECKING

from yarl import URL

from bot.apis import ApiIvrFi
from bot.ext import Context, Response, commands
from bot.utils import SessionsCaches, StringTools, UploadThings

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class PreviewCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot)
        self.StringTools: StringTools = StringTools()
        self.SessionsCaches: SessionsCaches = SessionsCaches(bot)
        self.ApiIvrFi = ApiIvrFi(bot, self.SessionsCaches.IvrFi.session)
        self.UploadThings: UploadThings = UploadThings(bot)

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: commands.Context) -> bool:  # NOQA
        return True

    @commands.command(name="preview", aliases=[])
    async def preview(self, ctx: Context, name: str) -> Response:
        translations = self.translations
        name = self.StringTools.str2name(name)
        if not name:
            return translations.Exceptions.user_not_provided(ctx)
        user_tmi = await self.bot.fetch_user(login=name)
        if not user_tmi:
            return translations.Exceptions.user_not_found_name(ctx, name)

        user_tmi = await self.ApiIvrFi.User.fetch_user(user_id=int(user_tmi.id))
        if not user_tmi:
            return translations.Exceptions.user_not_found_name(ctx, user_tmi)
        if not user_tmi.stream:
            return translations.Preview.not_live(ctx, name)

        twitch_url = URL("https://www.twitch.tv/")
        stream_started = user_tmi.stream.created_at
        stream2 = (await ctx.bot.fetch_videos(user_id=user_tmi.id))[0]
        now_adjusted = datetime.datetime.now().replace(tzinfo=None) - datetime.timedelta(seconds=90)
        vod_offset = (now_adjusted - stream_started).total_seconds()
        vod_offset = max(0, int(vod_offset))
        vod_url = (twitch_url / "videos" / stream2.id).update_query(t=f"{vod_offset}s")
        preview_img = await self.get_preview(name)
        return self.translations.Preview.preview(ctx, preview_img, vod_url)

    async def get_preview(self, name: str, tries=0) -> str:
        preview_url = self.bot.config.ApisConfig.clips_url / "preview" / name
        session = self.SessionsCaches.Clips.session

        preview_img = await session.get(str(preview_url))

        if "json" in preview_img.content_type and tries < 2:
            await asyncio.sleep(2)
            tries += 1
            return await self.get_preview(name)
        elif tries == 3:
            return "error"
        img = await preview_img.read()
        image = await self.UploadThings.upload_file(
            img,
            preview_img.content_type,
            filename=f"preview_{name}_{int(datetime.datetime.now().timestamp())}.jpg",
            session=session,
            url=self.bot.config.ApisConfig.feridinha_url,
            api_key={"token": self.bot.config.ApisConfig.feridinha_key},
        )
        return await self.UploadThings.shortener(image, ["preview"], session)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(PreviewCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
