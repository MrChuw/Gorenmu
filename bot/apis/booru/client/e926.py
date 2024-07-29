import json
import re
import time
from random import randint, shuffle

import aiohttp
from aiohttp_client_cache import CachedSession, RedisBackend, SQLiteBackend

from ..utils.parser import Api, better_object, deserialize, get_hostname, parse_image

Booru = Api()


class E926(object):
    """E926 wrapper

    Methods
    -------
    search : function
        Search and gets images from e926.

    get_image : function
        Gets images, meant just image urls from e926.

    """

    @staticmethod
    def append_obj(raw_object: dict):
        """Extends new object to the raw dict

        Parameters
        ----------
        raw_object : dict
            The raw object returned by e926.

        Returns
        -------
        str
            The new value of the raw object
        """
        for i in range(len(raw_object)):
            if "id" in raw_object[i]:
                raw_object[i]["post_url"] = f"{get_hostname(Booru.e926)}/posts/{raw_object[i]['id']}"

        return raw_object

    def __init__(self, cache: SQLiteBackend | RedisBackend, api_key: str = "", user_id: str = ""):
        """Initializes e926.

        Parameters
        ----------
        api_key : str
            Your API Key which is accessible within your account options page

        user_id : str
            Your user ID, which is accessible on the account options/profile page.
        """
        self.cache = cache

        if api_key and user_id == "":
            self.api_key = None
            self.user_id = None
        else:
            self.api_key = api_key
            self.user_id = user_id

        self.specs = {"api_key": self.api_key, "user_id": self.user_id}

    async def search(
        self,
        query: str,
        block: str = "",
        limit: int = 100,
        page: int = randint(0, 100),
        random: bool = True,
        gacha: bool = False,
    ):
        """Search and gets images from e926.

        Parameters
        ----------
        query : str
            The query to search for.

        block : str
            The disgusting query you want to block

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
            The json object returned by e926.
        """
        if gacha:
            limit = 100

        if limit > 1000:
            raise ValueError(Booru.error_handling_limit)

        if block and re.findall(block, query):
            raise ValueError(Booru.error_handling_sameval)

        if block != "":
            self.query = f"{query} -{block}*"

        else:
            self.query = query

        self.specs["tags"] = str(self.query)
        self.specs["limit"] = str(limit)
        self.specs["page"] = randint(0, 100)  # str(page)
        self.final = {"teste": 1}
        start_time = time.time()
        seconds = 12

        while self.final == {"teste": 1}:
            elapsed_time = time.time() - start_time
            if elapsed_time > seconds:
                return 1
            timeout = aiohttp.ClientTimeout(total=240)
            async with CachedSession(cache=self.cache, timeout=timeout) as session:
                async with session.get(
                    Booru.e926, params=self.specs, headers=Booru.headers, allow_redirects=True
                ) as resp:
                    self.data = await resp.text()
            self.final = self.final = deserialize(json.loads(self.data))
            self.final = self.final["posts"]
            if len(self.final) == 0:
                self.final = {"teste": 1}
            self.specs["page"] = randint(0, 5)

        if not self.final:
            raise ValueError(Booru.error_handling_null)

        self.not_random = E926.append_obj(self.final)
        shuffle(self.not_random)

        try:
            if gacha:
                return better_object(self.not_random[randint(0, len(self.not_random))])

            elif random:
                return better_object(self.not_random)

            else:
                return better_object(E926.append_obj(self.final))

        except Exception as e:
            raise ValueError(f"Failed to get data: {e}")

    async def get_image(self, query: str, block: str = "", limit: int = 100, page: int = randint(0, 100)):
        """Gets images, meant just image urls from e926.

        Parameters
        ----------
        query : str
            The query to search for.

        block : str
            The disgusting query you want to block

        limit : int
            The limit of images to return.

        page : int
            The number of desired page

        Returns
        -------
        list
            The list of image urls.

        """

        if limit > 1000:
            raise ValueError(Booru.error_handling_limit)

        if block and re.findall(block, query):
            raise ValueError(Booru.error_handling_sameval)

        if block != "":
            self.query = f"{query} -{block}*"

        else:
            self.query = query

        self.specs["tags"] = str(self.query)
        self.specs["limit"] = str(limit)
        self.specs["pid"] = str(page)
        self.specs["json"] = "1"
        self.final = {"teste": 1}

        try:
            timeout = aiohttp.ClientTimeout(total=240)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(
                    Booru.e926, params=self.specs, headers=Booru.headers, allow_redirects=True
                ) as resp:
                    self.data = await resp.text()
            self.final = self.final = deserialize(json.loads(self.data))

            self.not_random = parse_image(self.final)
            shuffle(self.not_random)
            return better_object(self.not_random)

        except:
            raise ValueError(f"Failed to get data")
