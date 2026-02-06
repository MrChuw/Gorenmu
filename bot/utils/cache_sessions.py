from __future__ import annotations

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
        self.Alias: SessionsCaches.Alias
        self.Color: SessionsCaches.Color
        self.Scp: SessionsCaches.Scp
        self.Wikihow: SessionsCaches.Wikihow
        self.Wikipedia: SessionsCaches.Wikipedia
        self.Safebooru: SessionsCaches.Safebooru
        self.Emotes: SessionsCaches.Emotes
        self.Translate: SessionsCaches.Translate
        self.Count: SessionsCaches.Count
        self.PixelSorting: SessionsCaches.PixelSorting
        self.ProfilePicture: SessionsCaches.ProfilePicture
        self.IvrFi: SessionsCaches.IvrFi
        self.Bug: SessionsCaches.Bug
        self.Suggest: SessionsCaches.Suggest
        self.Dicio: SessionsCaches.Dicio
        self.Clips: SessionsCaches.Clips
        self.RandomLine: SessionsCaches.RandomLine
        self.Nicks: SessionsCaches.Nicks
        self.Shorten: SessionsCaches.Shorten
        self.UserId: SessionsCaches.UserId
        self.Math: SessionsCaches.Math
        self.Interactive: SessionsCaches.Interactive
        for name, cls in vars(self.__class__).items():
            if isinstance(cls, type) and issubclass(cls, BaseCachedSession):
                setattr(self, name, cls(bot, useragent=self.UserAgent))  # NOQA

    async def close_all_sessions(self):
        for session in vars(self).values():
            if isinstance(session, BaseCachedSession):
                await session.close()

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
            return {"*.mrchuw.com.br/": timedelta(days=100), "https://api.mathjs.org": timedelta(days=100)}

    ToolsCachedSession: ToolsCachedSession

    class ImgurCachedSession(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, cache_name="Imgur_requests", useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {"*/*": timedelta(weeks=4 * 6)}

    ImgurCachedSession: ImgurCachedSession

    # region Hide.

    class Alias(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {self.alias_url: timedelta(days=100)}

    class Color(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {"thecolorapi.com/*": timedelta(days=30)}

    class Scp(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {"scp-wiki.wikidot.com/*": timedelta(weeks=4)}

    class Wikihow(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {"*.wikihow.com/*": timedelta(weeks=4)}

    class Wikipedia(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {"*.wikipedia.com/*": timedelta(weeks=4)}

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

    class Emotes(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            super().__init__(bot=bot, useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {
                "*7tv.io/v3/*": timedelta(minutes=15),
                "*api.betterttv.net/3/*": timedelta(minutes=15),
                "*api.frankerfacez.com/v1/*": timedelta(minutes=15),
            }

    class Translate(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {"https://translate.google.com/*": timedelta(weeks=4 * 6)}

    class Count(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {"*/*": timedelta(minutes=30)}

    class PixelSorting(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {"*/*": timedelta(hours=6)}

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

    class IvrFi(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {"https://*.ivr.fi/*": timedelta(minutes=10)}

    class Bug(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {}

    class Suggest(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {}

    class Dicio(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {self.bot.config.ApisConfig.dicio_url / "*": timedelta(hours=12)}

    class Clips(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {
                self.bot.config.ApisConfig.clips_url / "*": timedelta(seconds=15),
                self.feridinha_url: timedelta(hours=12),
            }

    class RandomLine(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {self.bot.config.ApisConfig.best_logs / "*": timedelta(microseconds=250)}

    class Nicks(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {self.bot.config.ApisConfig.best_logs / "*": timedelta(microseconds=250)}

    class Shorten(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {self.bot.config.ApisConfig.best_logs / "*": timedelta(microseconds=250)}

    # endregion

    class Weather(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {
                "nominatim.openstreetmap.org/*": timedelta(days=7),
                "api.open-meteo.com/v1/forecast": timedelta(minutes=10),
            }

    class UserId(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {self.bot.config.ApisConfig.best_logs / "*": timedelta(minutes=2)}

    class Math(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {self.bot.config.ApisConfig.pastebin_url / "*": timedelta(weeks=4)}

    class Interactive(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {"*": timedelta(minutes=10)}
