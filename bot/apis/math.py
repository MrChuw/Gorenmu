# -*- coding: utf-8 -*-
from dataclasses import dataclass

from aiohttp_client_cache import CachedSession, RedisBackend, SQLiteBackend


@dataclass
class Math:
    url: str = "http://localhost:12843/mathjs/evaluate"
    version: str = "v4"

    @classmethod
    async def evaluate(cls, expression: str, cache: SQLiteBackend | RedisBackend) -> str:
        url = f"{cls.url}/{cls.version}"
        payload = {"expression": expression, "precision": "14"}
        async with CachedSession(cache=cache) as session:
            response = await (await session.post(url, json=payload)).json()
        return response.get("result") or response.get("error")
