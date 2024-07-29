import json
from random import randint, shuffle

import aiohttp
from aiohttp_client_cache import CachedSession, RedisBackend, SQLiteBackend

from ..utils.parser import Api, better_object, deserialize, get_hostname, parse_image

Booru = Api()


# note: if your application rely on displaying images, you should implement a 'sync' stuff to behoimi.org itself
# these referer request just help you out to interacts with the API, not for displaying images


class Behoimi(object):
    """3d booru / Behoimi wrapper

    Methods
    -------
    search : function
        Search and gets images from behoimi.

    get_image : function
        Gets images, image urls only from behoimi.

    """

    @staticmethod
    async def mock(site: str, params: dict, cache):
        timeout = aiohttp.ClientTimeout(total=240)
        # async with aiohttp.ClientSession(timeout=timeout, headers=Booru.behoimi_bypass) as session:
        async with CachedSession(cache=cache, timeout=timeout, headers=Booru.behoimi_bypass) as session:
            async with session.get(site, params=params) as resp:
                bypass = await resp.text()
        return bypass

    @staticmethod
    def append_obj(raw_object: dict):
        """Extends new object to the raw dict

        Parameters
        ----------
        raw_object : dict
            The raw object returned by behoimi.

        Returns
        -------
        str
            The new value of the raw object
        """
        for i in range(len(raw_object)):
            if "id" in raw_object[i]:
                raw_object[i][
                    "post_url"
                ] = f"{get_hostname(Booru.behoimi)}/post/show/{raw_object[i]['id']}"

        return raw_object

    def __init__(self, cache: SQLiteBackend | RedisBackend):
        self.specs = {}
        self.cache = cache

    async def search(
        self,
        query: str,
        block: str = "",
        limit: int = 100,
        page: int = randint(0, 100),
        random: bool = True,
        gacha: bool = False,
    ):
        """Search and gets images from behoimi.

        Parameters
        ----------
        query : str
            The query to search for.

        limit : int
            The limit of images to return.

        page : int
            The number of desired page

        random : bool
            Shuffle the whole dict, default is True.

        gacha : bool
            Get random single object, limit property will be ignored.

        Returns
        -------
        dict
            The json object returned by behoimi.
        """
        if gacha:
            limit = 100

        if limit > 1000:
            raise ValueError(Booru.error_handling_limit)

        else:
            self.query = query

        self.specs["tags"] = str(self.query)
        self.specs["limit"] = str(limit)
        self.specs["page"] = str(page)

        self.data = await Behoimi.mock(Booru.behoimi, params=self.specs, cache=self.cache)
        if self.data == "[]":
            return 1
        self.final = self.final = deserialize(json.loads(self.data))

        if not self.final:
            raise ValueError(Booru.error_handling_null)

        self.not_random = Behoimi.append_obj(self.final)
        shuffle(self.not_random)

        try:
            if gacha:
                return better_object(self.not_random[randint(0, len(self.not_random))])

            elif random:
                return better_object(self.not_random)

            else:
                return better_object(Behoimi.append_obj(self.final))

        except Exception as e:
            raise ValueError(f"Failed to get data: {e}")

    async def get_image(self, query: str, limit: int = 100, page: int = randint(0, 100)):
        """Gets images, meant just image urls from behoimi.

        Parameters
        ----------
        query : str
            The query to search for.

        limit : int
            The limit of images to return.

        page : int
            The number of desired page

        Returns
        -------
        dict
            The json object returned by behoimi.

        """

        if limit > 1000:
            raise ValueError(Booru.error_handling_limit)

        else:
            self.query = query

        self.specs["tags"] = str(self.query)
        self.specs["limit"] = str(limit)
        self.specs["page"] = str(page)

        try:
            self.data = await Behoimi.mock(Booru.behoimi, params=self.specs)
            self.final = self.final = deserialize(json.loads(self.data))

            self.not_random = parse_image(self.final)
            shuffle(self.not_random)
            return better_object(self.not_random)

        except:
            raise ValueError(f"Failed to get data")
