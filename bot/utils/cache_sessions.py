# -*- coding: utf-8 -*-
from __future__ import annotations

import asyncio
from datetime import timedelta
from typing import TYPE_CHECKING

import aiohttp

from bot.utils.caches_base import BaseCachedSession
from bot.utils.singleton import Singleton

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class SessionsCaches(metaclass=Singleton):
    def __init__(self, bot: Gorenmu):
        self.UserAgent: str = "Mozilla/5.0 (compatible; Gorenmu/2.0; +https://github.com/MrChuw/Gorenmu)"
        for name, cls in vars(self.__class__).items():
            if isinstance(cls, type) and issubclass(cls, BaseCachedSession):
                setattr(self, name, cls(bot, useragent=self.UserAgent))  # NOQA

    async def close_all_sessions(self):
        for session in vars(self).values():
            if isinstance(session, BaseCachedSession):
                await session.close()

    def close(self):
        asyncio.create_task(self.close_all_sessions())

    # Old

    class AdminCachedSession(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            super().__init__(bot=bot, cache_name="Admin_requests", useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {"*.mrchuw.com.br/": timedelta(days=100), "static-cdn.jtvnw.net/previews-ttv/*": timedelta(days=1)}

    AdminCachedSession: AdminCachedSession

    class NSFWCachedSession(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            super().__init__(bot=bot, cache_name="NSFW_requests", useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {
                "https://gelbooru.com/": timedelta(hours=1),
                "https://rule34.xxx/": timedelta(hours=1),
                "https://tbib.org/": timedelta(hours=1),
                "https://safebooru.org/": timedelta(hours=1),
                "https://xbooru.com/": timedelta(hours=1),
                "https://realbooru.com/": timedelta(hours=1),
                "https://hypnohub.net/": timedelta(hours=1),
                "https://danbooru.donmai.us/": timedelta(hours=1),
                "https://booru.allthefallen.moe/": timedelta(hours=1),
                "https://yande.re/": timedelta(hours=1),
                "https://konachan.com/": timedelta(hours=1),
                "https://konachan.net/": timedelta(hours=1),
                "https://lolibooru.moe/": timedelta(hours=1),
                "https://e621.net/": timedelta(hours=1),
                "https://e926.net/": timedelta(hours=1),
                "https://derpibooru.org/": timedelta(hours=1),
                "https://furbooru.com/": timedelta(hours=1),
                "http://behoimi.org/": timedelta(hours=1),
                "https://rule34.paheal.net/": timedelta(hours=1),
            }

    NSFWCachedSession: NSFWCachedSession

    class ToolsCachedSession(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            super().__init__(bot=bot, cache_name="Tools_requests", useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {
                "*.mrchuw.com.br/": timedelta(days=100),
                "nominatim.openstreetmap.org/*": timedelta(days=7),
                "api.open-meteo.com/v1/forecast": timedelta(minutes=5),
                "https://api.mathjs.org": timedelta(days=100),
            }

    ToolsCachedSession: ToolsCachedSession

    class ImgurCachedSession(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, cache_name="Imgur_requests", useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {"*/*": timedelta(weeks=4 * 6)}

    ImgurCachedSession: ImgurCachedSession

    # New
    # region Hide.

    class Alias(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {self.alias_url: timedelta(days=100)}

    Alias: Alias

    class Color(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {"thecolorapi.com/*": timedelta(days=30)}

    Color: Color

    class Scp(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {"scp-wiki.wikidot.com/*": timedelta(weeks=4)}

    Scp: Scp

    class Wikihow(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {"*.wikihow.com/*": timedelta(weeks=4)}

    Wikihow: Wikihow

    class Wikipedia(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {"*.wikipedia.com/*": timedelta(weeks=4)}

    Wikipedia: Wikipedia

    class Safebooru(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            self.extra_headers = {"Alt-Used": "danbooru.donmai.us", "TE": "trailers"}
            self.timeout = aiohttp.ClientTimeout(total=240)
            super().__init__(bot=bot, useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {
                self.bot.config.ApisConfig.shlink_url.human_repr(): timedelta(hours=24),
                "https://safebooru.org/": timedelta(hours=1),
            }

    Safebooru: Safebooru

    class Emotes(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            super().__init__(bot=bot, useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {
                "*7tv.io/v3/*": timedelta(minutes=15),
                "*api.betterttv.net/3/*": timedelta(minutes=15),
                "*api.frankerfacez.com/v1/*": timedelta(minutes=15),
            }

    Emotes: Emotes

    class Translate(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {"https://translate.google.com/*": timedelta(weeks=4 * 6)}

    Translate: Translate

    class Count(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {"*/*": timedelta(minutes=30)}

    Count: Count

    class PixelSorting(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {"*/*": timedelta(hours=6)}

    PixelSorting: PixelSorting

    class ProfilePicture(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {
                "https://static-cdn.jtvnw.net/*": timedelta(hours=1),
                self.upload_url: timedelta(hours=12),
                self.shortener_url: timedelta(hours=12),
                self.feridinha_url: timedelta(hours=12),
            }

    ProfilePicture: ProfilePicture

    class IvrFi(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {"https://*.ivr.fi/*": timedelta(minutes=10)}

    IvrFi: IvrFi

    class Bug(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {}

    Bug: Bug

    # endregion

    class Suggest(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {}

    Suggest: Suggest

    class Dicio(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {self.bot.config.ApisConfig.dicio_url / "*": timedelta(hours=12)}

    Dicio: Dicio

    class Clips(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {
                self.bot.config.ApisConfig.clips_url / "*": timedelta(seconds=15),
                self.feridinha_url: timedelta(hours=12),
            }

    Clips: Clips

    class RandomLine(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {self.bot.config.ApisConfig.best_logs / "*": timedelta(microseconds=250)}

    RandomLine: RandomLine

    class Nicks(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {self.bot.config.ApisConfig.best_logs / "*": timedelta(microseconds=250)}

    Nicks: Nicks
