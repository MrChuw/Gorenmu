import json
import time
from random import randint, shuffle

import aiohttp
from aiohttp_client_cache import CachedSession, RedisBackend, SQLiteBackend
from xmltodict import parse

from ..utils.parser import Api, better_object

Booru = Api()


class Paheal(object):
    """paheal wrapper

    Methods
    -------
    search : function
        Search and gets images from paheal.

    get_image : function
        Gets images, meant just image urls from paheal.

    """

    def __init__(self, cache: SQLiteBackend | RedisBackend, api_key: str = "", user_id: str = ""):
        """Initializes paheal.

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
        """Search and gets images from paheal.

        Parameters
        ----------
        query : str
            The tags to search for.

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
            The json object returned by paheal.
        """
        if gacha:
            limit = 100

        if limit > 1000:
            raise ValueError(Booru.error_handling_limit)

        else:
            self.tags = query

        self.specs["tags"] = str(self.tags)
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
                async with session.get(Booru.paheal, params=self.specs, allow_redirects=True) as resp:
                    self.data = await resp.text()
            self.final = parse(self.data)
            self.final = json.dumps(self.final)
            self.final = json.loads(self.final)
            if self.final["posts"]["@count"] == "0":
                self.final = {"teste": 1}
            if self.final != {"teste": 1}:
                self.final = self.final["posts"]["tag"]
            self.specs["page"] = randint(0, 5)

        if len(self.final) == 0:
            raise ValueError(Booru.error_handling_null)

        self.not_random = self.final
        shuffle(self.not_random)

        try:
            if gacha:
                return better_object(self.final[randint(0, len(self.final))])

            elif random:
                return better_object(self.final)

            else:
                return better_object(self.not_random)

        except:
            raise ValueError(f"Failed to get data")

    async def get_image(self, query: str, limit: int = 100, page: int = randint(0, 100)):
        """Gets images, meant just image urls from paheal.

        Parameters
        ----------
        query : str
            The tags to search for.

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

        else:
            self.tags = query

        self.specs["tags"] = str(self.tags)
        self.specs["limit"] = str(limit)
        self.specs["page"] = str(page)

        try:
            timeout = aiohttp.ClientTimeout(total=240)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(Booru.paheal, params=self.specs, allow_redirects=True) as resp:
                    self.data = resp

            data_dict = parse(self.data.text)
            unsolved = json.dumps(data_dict)
            self.final = json.loads(unsolved, encoding="utf-8")

            abc_kontol = self.final
            ## extract all image urls
            self.image_urls = []
            for i in abc_kontol:  # paheal emang ngentot
                self.image_urls.append(i["@file_url"])

            shuffle(self.image_urls)
            return better_object(self.image_urls)

        except Exception as e:
            raise ValueError(f"Failed to get data: {e}")
