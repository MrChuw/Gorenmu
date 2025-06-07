# -*- coding: utf-8 -*-
from dataclasses import dataclass

import loguru
from aiohttp_client_cache import CachedSession


@dataclass
class Color:
    url: str = "https://www.thecolorapi.com/id"

    @classmethod
    async def name(cls, params: dict[str, str], session: CachedSession, log: loguru.logger) -> str | None:
        try:
            response = await (await session.get(cls.url, params=params)).json()
            return response["name"]["value"]
        except Exception as e:
            log.info(e)
            return None

    @classmethod
    async def hex(cls, nome: str, session: CachedSession) -> str:
        params = {"name": nome}
        response = await (await session.get(cls.url, params=params)).json()
        return response["hex"]["value"]
