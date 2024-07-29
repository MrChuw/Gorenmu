from dataclasses import dataclass

from datetime import timedelta

from aiohttp_client_cache import CachedSession, SQLiteBackend

urls_expire_after = {"thecolorapi.com": timedelta(days=30)}

allowed_methods = "GET"
cache = SQLiteBackend(
    cache_name=".cache/aiohttp-color-requests.db",
    urls_expire_after=urls_expire_after,
    allowed_methods=allowed_methods,
    include_headers=True,
)


@dataclass
class Color:
    url: str = "https://www.thecolorapi.com"

    @classmethod
    async def name(cls, hex_color: str) -> str:
        url = f"{cls.url}/id"
        params = {"hex": hex_color[1:] if hex_color[0] == "#" else hex_color}
        async with CachedSession(cache=cache) as session:
            response = await (await session.get(url, params=params)).json()
        return response["name"]["value"]
        # response = await CachedSession(cache=cache).get(url, params=params)
        # return response["name"]["value"]

    @classmethod
    async def hex(cls, nome: str) -> str:
        url = f"{cls.url}/id"
        params = {"name": nome}
        async with CachedSession(cache=cache) as session:
            response = await (await session.get(url, params=params)).json()
        return response["hex"]["value"]
        response = await CachedSession(cache=cache).get(url, params=params)
        return response["hex"]["value"]
