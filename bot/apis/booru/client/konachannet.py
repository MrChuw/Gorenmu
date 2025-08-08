from random import choice, randint, shuffle

from yarl import URL

from ..schemas import KonachannetElement, konachannet_from_dict
from ..utils import Api, SearchListType

Booru = Api()


class KonachanNet(SearchListType):
    """konachan net wrapper (SFW)

    Methods
    -------
    search : function
        Search and gets images from konachan net.

    get_image : function
        Gets images, image urls only from konachan net.

    """

    async def search(
        self,
        query: str,
        url: str = Booru.safebooru,
        block: str = "",
        limit: int = 100,
        page: int = randint(0, 100),
        gacha: bool = False,
    ) -> list[KonachannetElement] | None:
        """Search and gets images from konachan net.

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
            The json object returned by konachan net.
        """
        response = await self._search(url=url, query=query, block=block, limit=limit, page=page, gacha=gacha)
        if not response:
            return None
        response = konachannet_from_dict(response)
        return response

    async def random(
        self, query: str, block: str = "", limit: int = 100, page: int = randint(0, 100), gacha: bool = False
    ):
        results = await self.search(
            url=Booru.konachan_net, query=query, block=block, limit=limit, page=page, gacha=gacha
        )
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
