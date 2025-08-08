__version__ = "1.0.15"

from random import randint
from typing import List

from aiohttp_client_cache import CachedSession

from .classes import parser
from .classes.parser import (
    E621,
    E926,
    Atfbooru,
    Behoimi,
    Danbooru,
    Derpibooru,
    Furbooru,
    Gelbooru,
    Hypnohub,
    Konachan,
    Konachan_Net,
    Lolibooru,
    Paheal,
    Realbooru,
    Rule34,
    Safebooru,
    Tbib,
    Xbooru,
    Yandere,
)
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
from .client.konachannet import KonachanNet as Konachan_NetClient
from .client.lolibooru import Lolibooru as LolibooruClient
from .client.paheal import Paheal as PahealClient
from .client.realbooru import Realbooru as RealbooruClient
from .client.rule34 import Rule34 as Rule34Client
from .client.safebooru import Safebooru as SafebooruClient
from .client.tbib import Tbib as TbibClient
from .client.xbooru import Xbooru as XbooruClient
from .client.yandere import Yandere as YandereClient
from .utils.parser import resolve

# GelbooruClient = importlib.reload(GelbooruClient)

# TODO: Refazer isso, organizar melhor.


class Booru:
    def __init__(self):
        self.boorus = {
            "glbo": Booru.Gelbooru,
            "gelbooru": Booru.Gelbooru,  # NOQA
            "dnbo": Booru.Danbooru,
            "danbooru": Booru.Danbooru,  # NOQA
            "rule34": Booru.Rule34,  # NOQA
            "rlbo": Booru.Realbooru,
            "realbooru": Booru.Realbooru,  # NOQA
            "tbibo": Booru.Tbib,
            "tbib": Booru.Tbib,  # NOQA
            "xbbo": Booru.Xbooru,
            "xbooru": Booru.Xbooru,  # NOQA
            "sfbo": Booru.Safebooru,
            "safebooru": Booru.Safebooru,  # NOQA
            "ynbo": Booru.Yandere,
            "yandere": Booru.Yandere,  # NOQA
            "Knbo": Booru.Konachan,
            "konachan": Booru.Konachan,  # NOQA
            "hybo": Booru.Hypnohub,
            "hypnohub": Booru.Hypnohub,  # NOQA
            "e621bo": Booru.E621,
            "e621": Booru.E621,  # NOQA
            "e926bo": Booru.E926,
            "e926": Booru.E926,  # NOQA
            "dpbo": Booru.Derpibooru,
            "derpibooru": Booru.Derpibooru,  # NOQA
            "fubo": Booru.Furbooru,
            "furbooru": Booru.Furbooru,  # NOQA
            "bhbo": Booru.Behoimi,
            "behoimi": Booru.Behoimi,  # NOQA
            "phbo": Booru.Paheal,
            "paheal": Booru.Paheal,  # NOQA
            "knnbo": Booru.KonachanNet,
            "konachan_net": Booru.KonachanNet,  # NOQA
        }

    @classmethod
    async def search(
        cls, provider, query: str, block: str = "", limit: int = 100, page: int = randint(0, 100), gacha: bool = False
    ):
        result = await provider.search(query, block, limit, page, gacha)
        return result or None

    @classmethod
    async def random(
        cls, provider, query: str, block: str = "", limit: int = 100, page: int = randint(0, 300), gacha: bool = False
    ):
        image, preview = await provider.random(query, block, limit, page, gacha)
        return (None, None) if not image and not preview else (image, preview)

    def get_booru_instance(self, name):
        return getattr(self, name)

    class Gelbooru(GelbooruClient):

        def __init__(self, session: CachedSession, amount: int = 1):
            super().__init__(session, amount)

        @staticmethod
        def from_dict(data: dict):
            return Gelbooru(data)

        def from_dict_list(self, data: List[dict]):
            if isinstance(data, list):
                return [self.from_dict(item) for item in data]
            elif isinstance(data, dict):
                return self.from_dict(data)
            else:
                raise ValueError("Input must be a list or a dictionary.")

    class Rule34(Rule34Client):

        def __init__(self, session: CachedSession, amount: int = 1):
            super().__init__(session, amount)

        @staticmethod
        def from_dict(data: dict):
            return Rule34(data)

        def from_dict_list(self, data: List[dict]):
            if isinstance(data, list):
                return [self.from_dict(item) for item in data]
            elif isinstance(data, dict):
                return self.from_dict(data)
            else:
                raise ValueError("Input must be a list or a dictionary.")

    class Tbib(TbibClient):

        def __init__(self, session: CachedSession, amount: int = 1):
            super().__init__(session, amount)

        @staticmethod
        def from_dict(data: dict):
            return Tbib(data)

        def from_dict_list(self, data: List[dict]):
            if isinstance(data, list):
                return [self.from_dict(item) for item in data]
            elif isinstance(data, dict):
                return self.from_dict(data)
            else:
                raise ValueError("Input must be a list or a dictionary.")

    class Safebooru(SafebooruClient):

        def __init__(self, session: CachedSession | None, amount: int = 1):
            super().__init__(session, amount)

        @staticmethod
        def from_dict(data: dict):
            return Safebooru(data)

        def from_dict_list(self, data: List[dict]):
            if isinstance(data, list):
                return [self.from_dict(item) for item in data]
            elif isinstance(data, dict):
                return self.from_dict(data)
            else:
                raise ValueError("Input must be a list or a dictionary.")

    class Xbooru(XbooruClient):

        def __init__(self, session: CachedSession, amount: int = 1):
            super().__init__(session, amount)

        @staticmethod
        def from_dict(data: dict):
            return Xbooru(data)

        def from_dict_list(self, data: List[dict]):
            if isinstance(data, list):
                return [self.from_dict(item) for item in data]
            elif isinstance(data, dict):
                return self.from_dict(data)
            else:
                raise ValueError("Input must be a list or a dictionary.")

    class Realbooru(RealbooruClient):

        def __init__(self, session: CachedSession, amount: int = 1):
            super().__init__(session, amount)

        @staticmethod
        def from_dict(data: dict):
            return Realbooru(data)

        def from_dict_list(self, data: List[dict]):
            if isinstance(data, list):
                return [self.from_dict(item) for item in data]
            elif isinstance(data, dict):
                return self.from_dict(data)
            else:
                raise ValueError("Input must be a list or a dictionary.")

    class Hypnohub(HypnohubClient):

        def __init__(self, session: CachedSession, amount: int = 1):
            super().__init__(session, amount)

        @staticmethod
        def from_dict(data: dict):
            return Hypnohub(data)

        def from_dict_list(self, data: List[dict]):
            if isinstance(data, list):
                return [self.from_dict(item) for item in data]
            elif isinstance(data, dict):
                return self.from_dict(data)
            else:
                raise ValueError("Input must be a list or a dictionary.")

    class Danbooru(DanbooruClient):

        def __init__(self, session: CachedSession, amount: int = 1):
            super().__init__(session, amount)

        @staticmethod
        def from_dict(data: dict):
            return Danbooru(data)

        def from_dict_list(self, data: List[dict]):
            if isinstance(data, list):
                return [self.from_dict(item) for item in data]
            elif isinstance(data, dict):
                return self.from_dict(data)
            else:
                raise ValueError("Input must be a list or a dictionary.")

    class Yandere(YandereClient):

        def __init__(self, session: CachedSession, amount: int = 1):
            super().__init__(session, amount)

        @staticmethod
        def from_dict(data: dict):
            return Yandere(data)

        def from_dict_list(self, data: List[dict]):
            if isinstance(data, list):
                return [self.from_dict(item) for item in data]
            elif isinstance(data, dict):
                return self.from_dict(data)
            else:
                raise ValueError("Input must be a list or a dictionary.")

    class Konachan(KonachanClient):

        def __init__(self, session: CachedSession, amount: int = 1):
            super().__init__(session, amount)

        @staticmethod
        def from_dict(data: dict):
            return Konachan(data)

        def from_dict_list(self, data: List[dict]):
            if isinstance(data, list):
                return [self.from_dict(item) for item in data]
            elif isinstance(data, dict):
                return self.from_dict(data)
            else:
                raise ValueError("Input must be a list or a dictionary.")

    class KonachanNet(Konachan_NetClient):

        def __init__(self, session: CachedSession, amount: int = 1):
            super().__init__(session, amount)

        @staticmethod
        def from_dict(data: dict):
            return Konachan_Net(data)

        def from_dict_list(self, data: List[dict]):
            if isinstance(data, list):
                return [self.from_dict(item) for item in data]
            elif isinstance(data, dict):
                return self.from_dict(data)
            else:
                raise ValueError("Input must be a list or a dictionary.")

    class E621(E621Client):

        def __init__(self, session: CachedSession, amount: int = 1):
            super().__init__(session, amount)

        @staticmethod
        def from_dict(data: dict):
            return E621(data)

        def from_dict_list(self, data: List[dict]):
            if isinstance(data, list):
                return [self.from_dict(item) for item in data]
            elif isinstance(data, dict):
                return self.from_dict(data)
            else:
                raise ValueError("Input must be a list or a dictionary.")

    class E926(E926Client):

        def __init__(self, session: CachedSession, amount: int = 1):
            super().__init__(session, amount)

        @staticmethod
        def from_dict(data: dict):
            return E926(data)

        def from_dict_list(self, data: List[dict]):
            if isinstance(data, list):
                return [self.from_dict(item) for item in data]
            elif isinstance(data, dict):
                return self.from_dict(data)
            else:
                raise ValueError("Input must be a list or a dictionary.")

    class Derpibooru(DerpibooruClient):

        def __init__(self, session: CachedSession, amount: int = 1):
            super().__init__(session, amount)

        @staticmethod
        def from_dict(data: dict):
            return Derpibooru(data)

        def from_dict_list(self, data: List[dict]):
            if isinstance(data, list):
                return [self.from_dict(item) for item in data]
            elif isinstance(data, dict):
                return self.from_dict(data)
            else:
                raise ValueError("Input must be a list or a dictionary.")

    class Furbooru(FurbooruClient):

        def __init__(self, session: CachedSession, amount: int = 1):
            super().__init__(session, amount)

        @staticmethod
        def from_dict(data: dict):
            return Furbooru(data)

        def from_dict_list(self, data: List[dict]):
            if isinstance(data, list):
                return [self.from_dict(item) for item in data]
            elif isinstance(data, dict):
                return self.from_dict(data)
            else:
                raise ValueError("Input must be a list or a dictionary.")

    class Behoimi(BehoimiClient):

        def __init__(self, session: CachedSession, amount: int = 1):
            super().__init__(session, amount)

        @staticmethod
        def from_dict(data: dict):
            return Behoimi(data)

        def from_dict_list(self, data: List[dict]):
            if isinstance(data, list):
                return [self.from_dict(item) for item in data]
            elif isinstance(data, dict):
                return self.from_dict(data)
            else:
                raise ValueError("Input must be a list or a dictionary.")

    class Paheal(PahealClient):

        def __init__(self, session: CachedSession, amount: int = 1):
            super().__init__(session, amount)

        @staticmethod
        def from_dict(data: dict):
            return Paheal(data)

        def from_dict_list(self, data: List[dict]):
            if isinstance(data, list):
                return [self.from_dict(item) for item in data]
            elif isinstance(data, dict):
                return self.from_dict(data)
            else:
                raise ValueError("Input must be a list or a dictionary.")
