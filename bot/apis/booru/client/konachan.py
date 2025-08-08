from random import choice, randint, shuffle

from yarl import URL

from ..schemas import KonachanElement, konachan_from_dict
from ..utils import Api, SearchListType

Booru = Api()


class Konachan(SearchListType):
    """Konachan wrapper

    Methods
    -------
    search : function
        Search and gets images from konachan.

    get_image : function
        Gets images, image urls only from konachan.

    """

    async def search(
        self,
        query: str,
        url: str = Booru.safebooru,
        block: str = "",
        limit: int = 100,
        page: int = randint(0, 100),
        gacha: bool = False,
    ) -> list[KonachanElement] | None:
        """Search and gets images from konachan.

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
            The json object returned by konachan.
            :param gacha:
            :param page:
            :param limit:
            :param block:
            :param query:
            :param url:
        """
        response = await self._search(url=url, query=query, block=block, limit=limit, page=page, gacha=gacha)
        if not response:
            return None
        response = konachan_from_dict(response)
        return response

    async def random(
        self, query: str, block: str = "", limit: int = 100, page: int = randint(0, 100), gacha: bool = False
    ):
        results = await self.search(url=Booru.konachan, query=query, block=block, limit=limit, page=page, gacha=gacha)
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
