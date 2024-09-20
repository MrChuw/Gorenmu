from random import randint, shuffle, choice

from ..utils import SearchDictType, Api
from ..schemas import e621_from_dict, E621 as E621Schema
from yarl import URL

Booru = Api()


class E621(SearchDictType):
    """e621 wrapper

    Methods
    -------
    search : function
        Search and gets images from e621.

    get_image : function
        Gets images, meant just image urls from e621.

    """
    async def search(self, query: str, url: str = Booru.safebooru, block: str = "", limit: int = 100,
                     page: int = randint(0, 100), gacha: bool = False) -> E621Schema | None:
        """Search and gets images from e621.

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
            The json object returned by e621.
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
        response = e621_from_dict(response)
        return response


    async def random(self,
                     query: str,
                     block: str = "",
                     limit: int = 100,
                     page: int = randint(0, 100),
                     gacha: bool = False
                     ):
        results = await self.search(url=Booru.e621, query=query, block=block, limit=limit, page=page, gacha=gacha)
        if not results:
            return None, None
        shuffle(results.posts)

        if self.amount > 1:
            images = []
            images_preview = []
            for _ in range(self.amount):
                post = choice(results.posts)
                results.posts.remove(post)
                images.append(URL(post.file.url))
                images_preview.append(URL(post.preview.url))
            return images, images_preview

        post = choice(results.posts)
        return [URL(post.file.url)], [URL(post.preview.url)]
