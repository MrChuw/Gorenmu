from random import choice, randint, shuffle

from yarl import URL

from ..schemas import TbibElement, tbib_from_dict
from ..utils import Api, SearchListType

Booru = Api()


class Tbib(SearchListType):
    """Tbib wrapper

    Methods
    -------
    search : function
        Search and gets images from tbib.

    get_image : function
        Gets images, image urls only from tbib.

    """

    async def search(
        self,
        query: str,
        url: str = Booru.safebooru,
        block: str = "",
        limit: int = 100,
        page: int = randint(0, 100),
        gacha: bool = False,
    ) -> list[TbibElement] | None:
        """Search and gets images with raw data from tbib.

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
            The json object returned by tbib.
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
        response = tbib_from_dict(response)
        return response

    async def random(
        self, query: str, block: str = "", limit: int = 100, page: int = randint(0, 100), gacha: bool = False
    ):
        results = await self.search(url=Booru.tbib, query=query, block=block, limit=limit, page=page, gacha=gacha)
        if not results:
            return None, None
        shuffle(results)

        if self.amount > 1:
            images = []
            images_preview = []
            for _ in range(self.amount):
                post = choice(results)
                results.remove(post)
                images.append(URL(post.url))
                images_preview.append(URL(post.preview))
            return images, images_preview
        post = choice(results)
        return [URL(post.url)], [URL(post.preview)]
