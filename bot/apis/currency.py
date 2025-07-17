# -*- coding: utf-8 -*-
from dataclasses import dataclass

import loguru
from aiohttp_client_cache import CachedSession


@dataclass
class Currency:
    key: str
    url: str = "https://rest.coinapi.io"
    version: str = "v1"

    async def convert(self, base: str, to: str, session: CachedSession, log: loguru.logger) -> float | None:
        try:
            url = f"{self.url}/{self.version}/exchangerate/{base.upper()}/{to.upper()}"
            headers = {"Accept": "application/json", "X-CoinAPI-Key": self.key}
            response = await (await session.get(url, headers=headers)).json()
            return response["rate"]
        except Exception as e:
            log.info(e)
            return None
