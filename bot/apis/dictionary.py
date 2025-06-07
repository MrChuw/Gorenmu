# -*- coding: utf-8 -*-
from dataclasses import dataclass

import loguru
from aiohttp_client_cache import CachedSession


@dataclass
class Dictionary:
    url: str = "https://{}.wiktionary.org/w/api.php"

    @classmethod
    async def exists(cls, word: str, lang: str, session: CachedSession, log: loguru.logger) -> bool:
        params = {"action": "query", "titles": word, "format": "json", "formatversion": 2}  # NOQA

        try:
            data = await (await session.get(cls.url.format(lang), params=params)).json()
            pages = data.get("query", {}).get("pages", [])
            return pages and pages[0].get("missing") is not True
        except Exception as e:
            log.info(e)
            return False
