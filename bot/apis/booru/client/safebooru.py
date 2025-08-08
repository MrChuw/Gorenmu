from random import choice, randint, shuffle

from aiohttp import ClientResponse
from yarl import URL

from ..schemas import SafebooruElement, safebooru_from_dict
from ..utils import Api, SearchListType

Booru = Api()


class Safebooru(SearchListType):
    """Safebooru wrapper

    Methods
    -------
    search : function
        Search and gets images from safebooru.

    get_image : function
        Gets images, image urls only from safebooru.

    """

    async def search(
        self,
        query: str,
        url: str = Booru.safebooru,
        block: str = "",
        limit: int = 100,
        page: int = randint(0, 100),
        gacha: bool = False,
    ) -> list[SafebooruElement] | None:
        """Search and gets images from safebooru.

        Parameters
        ----------
        query : str
            The query to search for.

        block : str
            The disgusting query you want to block,
            e.g: you want to search 'erza_scarlet' but don't want to get furry, fill in 'furry'

        limit : int
            The limit of images to return.

        page : int
            The number of desired page

        gacha : bool
            Get random single object, limit property will be ignored.

        Returns
        -------
        dict
            The json object returned by safebooru.
            :param query:
            :param gacha:
            :param page:
            :param limit:
            :param block:
            :param url:
        """
        response = await self._search(url=url, query=query, block=block, limit=limit, page=page, gacha=gacha)
        if not response:
            return None
        response = safebooru_from_dict(response)
        return response

    async def random(
        self, query: str, block: str = "", limit: int = 100, page: int = randint(0, 100), gacha: bool = False
    ):
        results = await self.search(url=Booru.safebooru, query=query, block=block, limit=limit, page=page, gacha=gacha)
        if not results:
            return None, None
        shuffle(results)

        if self.amount > 1:
            images = []
            images_preview = []
            for _ in range(self.amount):
                post = choice(results)
                results.remove(post)
                images.append(URL(post.file_url))
                images_preview.append(URL(post.preview_url))
            return images, images_preview

        post = choice(results)
        return [URL(post.file_url)], [URL(post.preview_url)]

    async def get(
        self, query: str, block: str = "", limit: int = 100, page: int = randint(0, 100), gacha: bool = False
    ) -> ClientResponse:
        return await self._get(url=Booru.safebooru, query=query, block=block, limit=limit, page=page, gacha=gacha)
