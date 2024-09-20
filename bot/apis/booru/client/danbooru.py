from random import randint, shuffle, choice

from ..utils import SearchListType, Api
from ..schemas import danbooru_from_dict, DanbooruElement
from yarl import URL

Booru = Api()


class Danbooru(SearchListType):
    """Danbooru wrapper

    Methods
    -------
    search : function
        Search and gets images from danbooru.

    get_image : function
        Gets images, image urls only from danbooru.

    """
    async def search(self, query: str, url: str = Booru.danbooru, block: str = "", limit: int = 100,
                     page: int = randint(0, 100), gacha: bool = False) -> list[DanbooruElement] | None:
        """Search and gets images from danbooru.

        Parameters
        ----------
        query : str
            The query to search for.

        block : str
            The disgusting query you want to block,
            e.g: you want to search 'erza_scarlet' but dont want to gets furry, fill in 'furry'

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
            The json object returned by danbooru.
            :param block:
            :param limit:
            :param page:
            :param gacha:
            :param url:
        """
        response = await self._search(url=url, query=query, block=block, limit=limit, page=page, gacha=gacha)
        if not response:
            return None
        response = danbooru_from_dict(response)
        return response

    async def random(self,
                     query: str,
                     block: str = "",
                     limit: int = 100,
                     page: int = randint(0, 100),
                     gacha: bool = False
                     ):
        results = await self.search(url=Booru.danbooru, query=query, block=block, limit=limit, page=page, gacha=gacha)
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
                images_preview.append(URL(post.preview_file_url))
            return images, images_preview

        post = choice(results)
        return [URL(post.file_url)], [URL(post.preview_file_url)]