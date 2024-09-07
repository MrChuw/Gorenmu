from dataclasses import dataclass
from aiohttp_client_cache import CachedSession




@dataclass
class Color:
    url: str = "https://www.thecolorapi.com"

    @classmethod
    async def name(cls, hex_color: str, session: CachedSession) -> str:
        url = f"{cls.url}/id"
        params = {"hex": hex_color[1:] if hex_color[0] == "#" else hex_color}
        response = await (await session.get(url, params=params)).json()
        return response["name"]["value"]

    @classmethod
    async def hex(cls, nome: str, session: CachedSession) -> str:
        url = f"{cls.url}/id"
        params = {"name": nome}
        response = await (await session.get(url, params=params)).json()
        return response["hex"]["value"]
