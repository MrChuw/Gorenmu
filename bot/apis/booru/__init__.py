__version__ = "1.0.15"
import importlib
from random import randint

from aiohttp_client_cache import RedisBackend, SQLiteBackend

from .classes import parser
from .client.atfbooru import Atfbooru as AtfbooruClient
from .client.behoimi import Behoimi as BehoimiClient
from .client.danbooru import Danbooru as DanbooruClient
from .client.derpibooru import Derpibooru as DerpibooruClient
from .client.e621 import E621 as E621Client
from .client.e926 import E926 as E926Client
from .client.furbooru import Furbooru as FurbooruClient
from .client.gelbooru import Gelbooru as GelbooruClient
from .client.hypnohub import Hypnohub as HypnohubClient
from .client.konachan import Konachan as KonachanClient
from .client.konachan_net import Konachan_Net as Konachan_NetClient
from .client.lolibooru import Lolibooru as LolibooruClient
from .client.paheal import Paheal as PahealClient
from .client.realbooru import Realbooru as RealbooruClient
from .client.rule34 import Rule34 as Rule34Client
from .client.safebooru import Safebooru as SafebooruClient
from .client.tbib import Tbib as TbibClient
from .client.xbooru import Xbooru as XbooruClient
from .client.yandere import Yandere as YandereClient
from .utils.parser import resolve

importlib.reload(parser)

from .classes.parser import (
    Gelbooru,
    Rule34,
    Tbib,
    Safebooru,
    Xbooru,
    Realbooru,
    Hypnohub,
    Danbooru,
    Atfbooru,
    Yandere,
    Konachan,
    Konachan_Net,
    Lolibooru,
    E621,
    E926,
    Derpibooru,
    Furbooru,
    Behoimi,
    Paheal,
)

from typing import List

# TODO: Refazer isso, organizar melhor.

class Booru:
    def __init__(self):
        pass

    @classmethod
    async def search(
        cls,
        provider,
        query: str,
        block: str = "",
        limit: int = 100,
        page: int = randint(0, 100),
        random: bool = True,
        gacha: bool = False,
    ):
        result = await provider.search(query, block, limit, page, random, gacha, )
        if result == 1:
            return None
        parsed_result = resolve(result)
        return parsed_result

    def get_booru_instance(self, name):
        return getattr(self, name)

    class gelbooru(GelbooruClient):
        def __init__(self, cache: SQLiteBackend | RedisBackend):
            super().__init__(cache)

        def from_dict(cls, data: dict):
            return Gelbooru(data)

        def from_dict_list(self, data: List[dict]):
            if isinstance(data, list):
                return [self.from_dict(item) for item in data]
            elif isinstance(data, dict):
                return self.from_dict(data)
            else:
                raise ValueError("Input must be a list or a dictionary.")

    class rule34(Rule34Client):
        def __init__(self, cache: SQLiteBackend | RedisBackend):
            super().__init__(cache)

        def from_dict(cls, data: dict):
            return Rule34(data)

        def from_dict_list(self, data: List[dict]):
            if isinstance(data, list):
                return [self.from_dict(item) for item in data]
            elif isinstance(data, dict):
                return self.from_dict(data)
            else:
                raise ValueError("Input must be a list or a dictionary.")

    class tbib(TbibClient):
        def __init__(self, cache: SQLiteBackend | RedisBackend):
            super().__init__(cache)

        def from_dict(cls, data: dict):
            return Tbib(data)

        def from_dict_list(self, data: List[dict]):
            if isinstance(data, list):
                return [self.from_dict(item) for item in data]
            elif isinstance(data, dict):
                return self.from_dict(data)
            else:
                raise ValueError("Input must be a list or a dictionary.")

    class safebooru(SafebooruClient):
        def __init__(self, cache: SQLiteBackend | RedisBackend):
            super().__init__(cache)

        def from_dict(cls, data: dict):
            return Safebooru(data)

        def from_dict_list(self, data: List[dict]):
            if isinstance(data, list):
                return [self.from_dict(item) for item in data]
            elif isinstance(data, dict):
                return self.from_dict(data)
            else:
                raise ValueError("Input must be a list or a dictionary.")

    class xbooru(XbooruClient):
        def __init__(self, cache: SQLiteBackend | RedisBackend):
            super().__init__(cache)

        def from_dict(cls, data: dict):
            return Xbooru(data)

        def from_dict_list(self, data: List[dict]):
            if isinstance(data, list):
                return [self.from_dict(item) for item in data]
            elif isinstance(data, dict):
                return self.from_dict(data)
            else:
                raise ValueError("Input must be a list or a dictionary.")

    class realbooru(RealbooruClient):
        def __init__(self, cache: SQLiteBackend | RedisBackend):
            super().__init__(cache)

        def from_dict(cls, data: dict):
            return Realbooru(data)

        def from_dict_list(self, data: List[dict]):
            if isinstance(data, list):
                return [self.from_dict(item) for item in data]
            elif isinstance(data, dict):
                return self.from_dict(data)
            else:
                raise ValueError("Input must be a list or a dictionary.")

    class hypnohub(HypnohubClient):
        def __init__(self, cache: SQLiteBackend | RedisBackend):
            super().__init__(cache)

        def from_dict(cls, data: dict):
            return Hypnohub(data)

        def from_dict_list(self, data: List[dict]):
            if isinstance(data, list):
                return [self.from_dict(item) for item in data]
            elif isinstance(data, dict):
                return self.from_dict(data)
            else:
                raise ValueError("Input must be a list or a dictionary.")

    class danbooru(DanbooruClient):
        def __init__(self, cache: SQLiteBackend | RedisBackend):
            super().__init__(cache)

        def from_dict(cls, data: dict):
            return Danbooru(data)

        def from_dict_list(self, data: List[dict]):
            if isinstance(data, list):
                return [self.from_dict(item) for item in data]
            elif isinstance(data, dict):
                return self.from_dict(data)
            else:
                raise ValueError("Input must be a list or a dictionary.")

    class yandere(YandereClient):
        def __init__(self, cache: SQLiteBackend | RedisBackend):
            super().__init__(cache)

        def from_dict(cls, data: dict):
            return Yandere(data)

        def from_dict_list(self, data: List[dict]):
            if isinstance(data, list):
                return [self.from_dict(item) for item in data]
            elif isinstance(data, dict):
                return self.from_dict(data)
            else:
                raise ValueError("Input must be a list or a dictionary.")

    class konachan(KonachanClient):
        def __init__(self, cache: SQLiteBackend | RedisBackend):
            super().__init__(cache)

        def from_dict(cls, data: dict):
            return Konachan(data)

        def from_dict_list(self, data: List[dict]):
            if isinstance(data, list):
                return [self.from_dict(item) for item in data]
            elif isinstance(data, dict):
                return self.from_dict(data)
            else:
                raise ValueError("Input must be a list or a dictionary.")

    class konachan_net(Konachan_NetClient):
        def __init__(self, cache: SQLiteBackend | RedisBackend):
            super().__init__(cache)

        def from_dict(cls, data: dict):
            return Konachan_Net(data)

        def from_dict_list(self, data: List[dict]):
            if isinstance(data, list):
                return [self.from_dict(item) for item in data]
            elif isinstance(data, dict):
                return self.from_dict(data)
            else:
                raise ValueError("Input must be a list or a dictionary.")

    class e621(E621Client):
        def __init__(self, cache: SQLiteBackend | RedisBackend):
            super().__init__(cache)

        def from_dict(cls, data: dict):
            return E621(data)

        def from_dict_list(self, data: List[dict]):
            if isinstance(data, list):
                return [self.from_dict(item) for item in data]
            elif isinstance(data, dict):
                return self.from_dict(data)
            else:
                raise ValueError("Input must be a list or a dictionary.")

    class e926(E926Client):
        def __init__(self, cache: SQLiteBackend | RedisBackend):
            super().__init__(cache)

        def from_dict(cls, data: dict):
            return E926(data)

        def from_dict_list(self, data: List[dict]):
            if isinstance(data, list):
                return [self.from_dict(item) for item in data]
            elif isinstance(data, dict):
                return self.from_dict(data)
            else:
                raise ValueError("Input must be a list or a dictionary.")

    class derpibooru(DerpibooruClient):
        def __init__(self, cache: SQLiteBackend | RedisBackend):
            super().__init__(cache)

        def from_dict(cls, data: dict):
            return Derpibooru(data)

        def from_dict_list(self, data: List[dict]):
            if isinstance(data, list):
                return [self.from_dict(item) for item in data]
            elif isinstance(data, dict):
                return self.from_dict(data)
            else:
                raise ValueError("Input must be a list or a dictionary.")

    class furbooru(FurbooruClient):
        def __init__(self, cache: SQLiteBackend | RedisBackend):
            super().__init__(cache)

        def from_dict(cls, data: dict):
            return Furbooru(data)

        def from_dict_list(self, data: List[dict]):
            if isinstance(data, list):
                return [self.from_dict(item) for item in data]
            elif isinstance(data, dict):
                return self.from_dict(data)
            else:
                raise ValueError("Input must be a list or a dictionary.")

    class behoimi(BehoimiClient):
        def __init__(self, cache: SQLiteBackend | RedisBackend):
            super().__init__(cache)

        def from_dict(cls, data: dict):
            return Behoimi(data)

        def from_dict_list(self, data: List[dict]):
            if isinstance(data, list):
                return [self.from_dict(item) for item in data]
            elif isinstance(data, dict):
                return self.from_dict(data)
            else:
                raise ValueError("Input must be a list or a dictionary.")

    class paheal(PahealClient):
        def __init__(self, cache: SQLiteBackend | RedisBackend):
            super().__init__(cache)

        def from_dict(cls, data: dict):
            return Paheal(data)

        def from_dict_list(self, data: List[dict]):
            if isinstance(data, list):
                return [self.from_dict(item) for item in data]
            elif isinstance(data, dict):
                return self.from_dict(data)
            else:
                raise ValueError("Input must be a list or a dictionary.")


