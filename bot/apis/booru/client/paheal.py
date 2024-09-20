import time
from random import randint, shuffle, choice
from bs4 import BeautifulSoup

from aiohttp_client_cache import CachedSession

from ..utils.parser import Api
from yarl import URL

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

    def __init__(self, session: CachedSession, amount: int):
        self.session = session
        self.amount: int = amount
        self.specs = {}
        self.data: str | None = None
        self.query: str | None = None
        self.img: URL | None = None
        self.preview: URL | None = None

    async def search(self, url: str, tag: str = "", page: int = randint(0, 300)):
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
            :param page:
            :param tag:
            :param url:
        """

        start_time = time.time()
        seconds = 12

        url_request = f"{url}/post/list/"

        if tag := tag.replace(" ", "_"):
            url_request += tag

        url_request += str(page)

        while not self.img or not self.preview:
            elapsed_time = time.time() - start_time
            if elapsed_time > seconds:
                return None
            self.response = await self.session.get(url_request, allow_redirects=True)
            self.data = await self.response.text()
            soup = BeautifulSoup(self.data, "html.parser")
            thumb_links = soup.find_all("div", class_="shm-thumb thumb")
            random_thumb_link = choice(thumb_links)
            self.img = random_thumb_link.find("a", text="File Only")['href'] if random_thumb_link.find("a", text="File Only") else None
            self.preview = url + random_thumb_link.find("img")["src"]
        return True


    async def random(self,
                     query: str,
                     block: str = "",
                     limit: int = 100,
                     page: int = randint(0, 300),
                     gacha: bool = False
                     ):
        if self.amount > 1:
            images = []
            images_preview = []
            for _ in range(self.amount):
                self.img = None
                self.preview = None
                response = await self.search(url=Booru.paheal, tag=query, page=page)
                if not response:
                    return None, None
                page = page + 1 if page < 100 else page - 1
                images.append(URL(self.img))
                images_preview.append(URL(self.preview))
            return images, images_preview

        response = await self.search(url=Booru.paheal, tag=query, page=page)
        return ([URL(self.img)], [URL(self.preview)]) if response else (None, None)
