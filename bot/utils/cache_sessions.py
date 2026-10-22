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
        self.Alias: Alias = Alias(bot=bot, useragent=self.UserAgent)
        self.Color: Color = Color(bot=bot, useragent=self.UserAgent)
        self.Scp: Scp = Scp(bot=bot, useragent=self.UserAgent)
        self.Wikihow: Wikihow = Wikihow(bot=bot, useragent=self.UserAgent)
        self.Wikipedia: Wikipedia = Wikipedia(bot=bot, useragent=self.UserAgent)
        self.Safebooru: Safebooru = Safebooru(bot=bot, useragent=self.UserAgent)
        self.Emotes: Emotes = Emotes(bot=bot, useragent=self.UserAgent)
        self.Translate: Translate = Translate(bot=bot, useragent=self.UserAgent)
        self.Count: Count = Count(bot=bot, useragent=self.UserAgent)
        self.PixelSorting: PixelSorting = PixelSorting(bot=bot, useragent=self.UserAgent)
        self.ProfilePicture: ProfilePicture = ProfilePicture(bot=bot, useragent=self.UserAgent)
        self.IvrFi: IvrFi = IvrFi(bot=bot, useragent=self.UserAgent)
        self.Bug: Bug = Bug(bot=bot, useragent=self.UserAgent)
        self.Suggest: Suggest = Suggest(bot=bot, useragent=self.UserAgent)
        self.Dicio: Dicio = Dicio(bot=bot, useragent=self.UserAgent)
        self.Clips: Clips = Clips(bot=bot, useragent=self.UserAgent)
        self.RandomLine: RandomLine = RandomLine(bot=bot, useragent=self.UserAgent)
        self.Nicks: Nicks = Nicks(bot=bot, useragent=self.UserAgent)
        self.Shorten: Shorten = Shorten(bot=bot, useragent=self.UserAgent)
        self.Weather: Weather = Weather(bot=bot, useragent=self.UserAgent)
        self.UserId: UserId = UserId(bot=bot, useragent=self.UserAgent)
        self.Math: Math = Math(bot=bot, useragent=self.UserAgent)
        self.Interactive: Interactive = Interactive(bot=bot, useragent=self.UserAgent)
        self.Imgur: Imgur = Imgur(bot=bot, useragent=self.UserAgent)
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
            "https://behoimi.org/": timedelta(hours=1),
            "https://rule34.paheal.net/": timedelta(hours=1),
        }


class ToolsCachedSession(BaseCachedSession):
    def __init__(self, bot: Gorenmu, useragent: str):
        super().__init__(bot=bot, cache_name="Tools_requests", useragent=useragent)

    def get_expiry_times(self) -> dict:
        return {"*.mrchuw.com.br/": timedelta(days=100), "https://api.mathjs.org": timedelta(days=100)}


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
        headers = {
            "User-Agent": "Gorenmu/2.0 (+https://github.com/MrChuw/Gorenmu)",
            "Accept": "*/*",
            "Connection": "close",
        }
        super().__init__(bot=bot, useragent=useragent, headers=headers)

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
        return {
                self.bot.config.ApisConfig.pastebin_url / "*": timedelta(weeks=4),
                "https://api.mathjs.org/v4/*": timedelta(days=30)
        }


class Interactive(BaseCachedSession):
    def __init__(self, bot: Gorenmu, useragent: str):
        self.allowed_codes = (200,)
        super().__init__(bot=bot, useragent=useragent)

    def get_expiry_times(self) -> dict:
        return {"*": timedelta(minutes=10)}


class Imgur(BaseCachedSession):
    def __init__(self, bot: Gorenmu, useragent: str):
        self.allowed_codes = (200, 202)
        headers = {
            "User-Agent": useragent,
            "Priority": "u=0, i",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
        }
        super().__init__(bot=bot, useragent=useragent, headers=headers)

    def get_expiry_times(self) -> dict:
        return {"*/*": timedelta(weeks=4 * 6)}
