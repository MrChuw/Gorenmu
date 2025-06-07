# -*- coding: utf-8 -*-
from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING

import aiohttp

from bot.utils.caches_base import BaseCachedSession

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class SessionsCaches:
    def __init__(self, bot):
        self.UserAgent: str = "Mozilla/5.0 (compatible; Gorenmu/2.0; +https://github.com/MrChuw/Gorenmu)"
        for name, cls in vars(self.__class__).items():
            if isinstance(cls, type) and issubclass(cls, BaseCachedSession):
                setattr(self, name, cls(bot, useragent=self.UserAgent))  # NOQA

    async def close_all_sessions(self):
        for session in vars(self).values():
            if isinstance(session, BaseCachedSession):
                await session.close()

    class AdminCachedSession(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            super().__init__(bot=bot, cache_name="Admin_requests", useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {
                "*.mrchuw.com.br/": timedelta(days=100),
                "im.mrchuw.com.br/api/files/*": timedelta(days=100),
                "static-cdn.jtvnw.net/previews-ttv/*": timedelta(days=1),
            }

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

    class RandomCachedSession(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            super().__init__(bot=bot, cache_name="Random_requests", useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {
                "*.imgur.com/*": timedelta(days=200),
                "scp-wiki.wikidot.com": -1,
                "https://pt.wikihow.com/Especial:Randomizer": 1,
                "https://pt.wikipedia.org/wiki/Special:Random": 1,
            }

    RandomCachedSession: RandomCachedSession

    class GeneralCachedSession(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            super().__init__(bot=bot, cache_name="General_requests", useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {"*.dicio.com": timedelta(days=120)}

    GeneralCachedSession: GeneralCachedSession

    class InfoCachedSession(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            super().__init__(bot=bot, cache_name="Info_requests", useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {"*.jtvnw.net/*": timedelta(minutes=30)}

    InfoCachedSession: InfoCachedSession

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

    class AliasCachedSession(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, cache_name="Alias_requests", useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {"*/*": -1}

    AliasCachedSession: AliasCachedSession

    class CountCachedSession(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, cache_name="Count_requests", useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {"*/*": timedelta(minutes=30)}

    CountCachedSession: CountCachedSession

    class TranslateCachedSession(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, cache_name="Translate_requests", useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {"*/*": timedelta(weeks=4 * 6)}

    TranslateCachedSession: TranslateCachedSession

    class ImgurCachedSession(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, cache_name="Imgur_requests", useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {"*/*": timedelta(weeks=4 * 6)}

    ImgurCachedSession: ImgurCachedSession

    class ColorCachedSession(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, cache_name="Color_requests", useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {"thecolorapi.com": timedelta(days=30)}

    ColorCachedSession: ColorCachedSession

    class ScpCachedSession(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, cache_name="Scp_requests", useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {"scp-wiki.wikidot.com/*": timedelta(weeks=4)}

    ScpCachedSession: ScpCachedSession

    class WikihowCachedSession(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, cache_name="Wikihow_requests", useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {"*.wikihow.com/*": timedelta(weeks=4)}

    WikihowCachedSession: WikihowCachedSession

    class WikipediaCachedSession(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, cache_name="Wikipedia_requests", useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {"*.wikipedia.com/*": timedelta(weeks=4)}

    WikipediaCachedSession: WikipediaCachedSession

    class BooruCachedSession(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            self.allowed_codes = (200,)
            self.extra_headers = {"Alt-Used": "danbooru.donmai.us", "TE": "trailers"}
            self.timeout = aiohttp.ClientTimeout(total=240)
            super().__init__(bot=bot, cache_name="Booru_requests", useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {
                self.bot.config.ApisConfig.shlink_url: timedelta(hours=24),
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

    BooruCachedSession: BooruCachedSession

    class EmotesCachedSession(BaseCachedSession):
        def __init__(self, bot: Gorenmu, useragent: str):
            super().__init__(bot=bot, cache_name="Emotes_requests", useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {
                "*7tv.io/v3/*": timedelta(minutes=15),
                "*api.betterttv.net/3/*": timedelta(minutes=15),
                "*api.frankerfacez.com/v1/*": timedelta(minutes=15),
            }

    EmotesCachedSession: EmotesCachedSession
