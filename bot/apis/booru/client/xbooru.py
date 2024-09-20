from random import randint, shuffle, choice

from ..utils import SearchListType, Api
from ..schemas import xbooru_from_dict, XbooruElement
from yarl import URL

Booru = Api()


class Xbooru(SearchListType):
    """Xbooru wrapper

    Methods
    -------
    search : function
        Search and gets images from xbooru.

    get_image : function
        Gets images, image urls only from xbooru.

    """
    async def search(self, query: str, url: str = Booru.safebooru, block: str = "", limit: int = 100,
                     page: int = randint(0, 100), gacha: bool = False) -> list[XbooruElement] | None:
        """Search and gets images with raw data from xbooru.

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
            The json object returned by xbooru.

        """
        response = await self._search(url=url, query=query, block=block, limit=limit, page=page, gacha=gacha)
        if not response:
            return None
        response = xbooru_from_dict(response)
        return response

    async def random(self, query: str, block: str = "", limit: int = 100, page: int = randint(0, 100),
                     gacha: bool = False
                     ):
        results = await self.search(url=Booru.xbooru, query=query, block=block, limit=limit, page=page, gacha=gacha)
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
