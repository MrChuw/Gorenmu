import json
import pickle
import time
from random import randint, shuffle

import aiohttp
import numpy as np
from aiohttp_client_cache import CachedSession, RedisBackend, SQLiteBackend

from ..utils.parser import Api, better_object, deserialize, get_hostname

Booru = Api()


class Derpibooru(object):
    """derpibooru wrapper

    Methods
    -------
    search : function
        Search and gets images from derpibooru.

    get_image : function
        Gets images, image urls only from derpibooru.

    """

    @staticmethod
    def append_obj(raw_object: dict):
        """Extends new object to the raw dict

        Parameters
        ----------
        raw_object : dict
            The raw object returned by derpibooru.

        Returns
        -------
        str
            The new value of the raw object
        """
        for i in range(len(raw_object)):
            if "id" in raw_object[i]:
                raw_object[i]["post_url"] = f"{get_hostname(Booru.derpibooru)}/images/{raw_object[i]['id']}"

        return raw_object

    def __init__(self, cache: SQLiteBackend | RedisBackend, key: str = ""):
        """Initializes derpibooru.

        Parameters
        ----------
        key : str
            An optional authentication token. If omitted, no user will be authenticated.
        """

        self.cache = cache
        if key:
            self.key = None
        else:
            self.key = key

        self.specs = {"key": self.key}

    async def search(
        self,
        query: str,
        block: str = "",
        limit: int = 100,
        page: int = randint(0, 100),
        random: bool = True,
        gacha: bool = False,
    ):
        """Search and gets images from derpibooru.

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
            The json object returned by derpibooru.
        """
        if gacha:
            limit = 100

        if limit > 1000:
            raise ValueError(Booru.error_handling_limit)

        else:
            self.query = query

        self.specs["q"] = str(self.query)
        self.specs["per_page"] = str(limit)
        self.specs["page"] = randint(0, 100)  # str(page)
        self.final = {"teste": 1}
        start_time = time.time()
        seconds = 12
        path = f"./data/"
        if self.specs["q"] == "":
            with open(path + "derpibooru_tags.pickle", "rb") as fp:
                tags = pickle.load(fp)
            self.specs["q"] = np.random.choice(tags)

        while self.final == {"teste": 1}:
            elapsed_time = time.time() - start_time
            if elapsed_time > seconds:
                return 1
            timeout = aiohttp.ClientTimeout(total=240)
            async with CachedSession(cache=self.cache, timeout=timeout) as session:
                async with session.get(Booru.derpibooru, params=self.specs, allow_redirects=True) as resp:
                    self.data = await resp.text()
            self.final = deserialize(json.loads(self.data))
            self.final = self.final["images"]
            if len(self.final) == 0:
                self.final = {"teste": 1}
            self.specs["page"] = randint(0, 5)

        if not self.final:
            raise ValueError(Booru.error_handling_null)

        self.not_random = Derpibooru.append_obj(self.final)
        shuffle(self.not_random)

        try:
            if gacha:
                return better_object(self.not_random[randint(0, len(self.not_random))])

            elif random:
                return better_object(self.not_random)

            else:
                return better_object(Derpibooru.append_obj(self.final))

        except Exception as e:
            raise ValueError(f"Failed to get data: {e}")

    async def get_image(self, query: str, limit: int = 100, page: int = randint(0, 100)):
        """Gets images, meant just image urls from derpibooru.

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
            The json object returned by derpibooru.

        """

        if limit > 1000:
            raise ValueError(Booru.error_handling_limit)

        else:
            self.query = query

        self.specs["q"] = str(self.query)
        self.specs["per_page"] = str(limit)
        self.specs["page"] = str(page)

        try:
            timeout = aiohttp.ClientTimeout(total=240)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(Booru.derpibooru, params=self.specs, allow_redirects=True) as resp:
                    self.data = await resp.text()
            self.final = self.final = deserialize(json.loads(self.data))

            self.not_random = [i["representations"]["full"] for i in self.final]
            shuffle(self.not_random)
            return better_object(self.not_random)

        except:
            raise ValueError(f"Failed to get data")
