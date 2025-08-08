import pickle
from random import choice, randint, shuffle

from yarl import URL

from ..schemas import Furbooru as FurbooruSchema
from ..schemas import furbooru_from_dict
from ..utils import Api, SearchDictType2

Booru = Api()


class Furbooru(SearchDictType2):
    """furbooru wrapper

    Methods
    -------
    search : function
        Search and gets images from furbooru.

    get_image : function
        Gets images, image urls only from furbooru.

    """

    async def search(
        self,
        query: str,
        url: str = Booru.safebooru,
        block: str = "",
        limit: int = 100,
        page: int = randint(0, 100),
        gacha: bool = False,
    ) -> FurbooruSchema | None:
        """Search and gets images from furbooru.

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
            The json object returned by furbooru.
        """

        with open("./bot/apis/booru/utils/furbooru_tags.pickle", "rb") as fp:
            tags = pickle.load(fp)
        query = query or choice(tags)
        response = await self._search(url=url, query=query, block=block, limit=limit, page=page, gacha=gacha)
        if not response:
            return None
        response = furbooru_from_dict(response)
        return response

    async def random(
        self, query: str, block: str = "", limit: int = 100, page: int = randint(0, 100), gacha: bool = False
    ):
        results = await self.search(url=Booru.derpibooru, query=query, block=block, limit=limit, page=page, gacha=gacha)
        if not results:
            return None, None
        shuffle(results.images)

        if self.amount > 1:
            if len(results.images) < self.amount:
                self.amount = len(results.images)
            images = []
            images_preview = []
            for _ in range(self.amount):
                post = choice(results.images)
                results.images.remove(post)
                images.append(URL(post.representations.full))
                images_preview.append(URL(post.representations.thumb))
            return images, images_preview

        post = choice(results.images)
        return [URL(post.representations.full)], [URL(post.representations.thumb)]
