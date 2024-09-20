from random import randint, shuffle, choice

from ..utils import SearchDictType, Api
from ..schemas import gelbooru_from_dict, Gelbooru as GelbooruSchema
from yarl import URL

Booru = Api()


class Gelbooru(SearchDictType):
    """Gelbooru wrapper

    Methods
    -------
    search : function
        Search and gets images from gelbooru.

    get_image : function
        Gets images, meant just image urls from gelbooru.

    """
    async def search(self, query: str, url: str = Booru.safebooru, block: str = "", limit: int = 100,
                     page: int = randint(0, 100), gacha: bool = False) -> GelbooruSchema | None:
        """Search and gets images from gelbooru.

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

        random : bool
            Shuffle the whole dict, default is True.

        gacha : bool
            Get random single object, limit property will be ignored.

        Returns
        -------
        dict
            The json object returned by gelbooru.
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
        response = gelbooru_from_dict(response)
        return response

    async def random(
        self,
        query: str,
        block: str = "",
        limit: int = 100,
        page: int = randint(0, 100),
        gacha: bool = False
    ):
        results = await self.search(url=Booru.gelbooru, query=query, block=block, limit=limit, page=page, gacha=gacha)
        if not results:
            return None, None
        shuffle(results.post)

        if self.amount > 1:
            images = []
            images_preview = []
            for _ in range(self.amount):
                post = choice(results.post)
                results.post.remove(post)
                images.append(URL(post.file_url))
                images_preview.append(URL(post.preview_url))
            return images, images_preview

        post = choice(results.post)
        return [URL(post.file_url)], [URL(post.preview_url)]



