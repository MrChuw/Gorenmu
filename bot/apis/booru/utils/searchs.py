import json
import re
import time
from random import randint

from aiohttp import ClientResponse
from aiohttp_client_cache import CachedSession

from ..utils.parser import Api

Booru = Api()


class SearchListType(object):
    def __init__(self, session: CachedSession, amount: int, api_key: str = None, user_id: str = None):
        self.session = session
        self.amount: int = amount

        if api_key or user_id:
            self.api_key = api_key
            self.user_id = user_id
            self.specs = {"api_key": self.api_key, "user_id": self.user_id}
        else:
            self.specs = {}

        self.data: str | None = None
        self.query: str | None = None
        self.final: list[object] | None = None

    async def _search(
        self,
        url: str,
        query: str,
        block: str = "",
        limit: int = 100,
        page: int = randint(0, 100),
        gacha: bool = False,
    ) -> list[object] | None:
        if gacha:
            limit = 100

        if limit > 1000:
            raise ValueError(Booru.error_handling_limit)

        if block and re.findall(block, query):
            raise ValueError(Booru.error_handling_sameval)

        self.query = f"{query} -{block}*" if block != "" else query
        self.specs["tags"] = str(self.query)
        self.specs["limit"] = str(limit)
        self.specs["pid"] = str(page)
        self.specs["json"] = "1"
        self.final = {"teste": 1}
        start_time = time.time()
        seconds = 12

        while self.final == {"teste": 1}:
            elapsed_time = time.time() - start_time
            if elapsed_time > seconds:
                return None
            self.response = await self.session.get(url, params=self.specs, allow_redirects=True)
            self.data = await self.response.text()
            try:
                self.final = json.loads(self.data)
            except Exception as e:
                return None
            if len(self.final) == 0:
                self.final = {"teste": 1}
            self.specs["pid"] = randint(0, 5)

        if not self.final:
            raise ValueError(Booru.error_handling_null)

        return self.final

    async def _get(
        self, url: str, query: str, block: str = "", limit: int = 100, page: int = randint(0, 100), gacha: bool = False
    ) -> ClientResponse:
        if gacha:
            limit = 100

        if limit > 1000:
            raise ValueError(Booru.error_handling_limit)

        if block and re.findall(block, query):
            raise ValueError(Booru.error_handling_sameval)

        self.query = f"{query} -{block}*" if block != "" else query
        self.specs["tags"] = str(self.query)
        self.specs["limit"] = str(limit)
        self.specs["pid"] = str(page)
        self.specs["json"] = "1"
        self.final = {"teste": 1}
        return await self.session.get(url, params=self.specs, allow_redirects=True)


class SearchListType2(object):
    def __init__(self, session: CachedSession, amount: int):
        self.session = session
        self.amount: int = amount
        self.specs = {}

        self.data: str | None = None
        self.query: str | None = None
        self.final: list[object] | None = None

    async def _search(
        self,
        url: str,
        query: str,
        block: str = "",
        limit: int = 100,
        page: int = randint(0, 100),
        gacha: bool = False,
    ) -> list[object] | None:
        if gacha:
            limit = 100

        if limit > 1000:
            raise ValueError(Booru.error_handling_limit)

        if block and re.findall(block, query):
            raise ValueError(Booru.error_handling_sameval)

        self.query = f"{query} -{block}*" if block != "" else query

        self.specs["tags"] = str(self.query)
        self.specs["limit"] = str(limit)
        self.specs["page"] = str(page)
        self.final = {"teste": 1}
        start_time = time.time()
        seconds = 12

        while self.final == {"teste": 1}:
            elapsed_time = time.time() - start_time
            if elapsed_time > seconds:
                return None
            self.response = await self.session.get(url, params=self.specs, allow_redirects=True)
            self.data = await self.response.text()
            try:
                self.final = json.loads(self.data)
            except Exception as e:
                return None
            if len(self.final) == 0:
                self.final = {"teste": 1}
            self.specs["page"] = randint(0, 5)

        if not self.final:
            raise ValueError(Booru.error_handling_null)

        return self.final


class SearchDictType(object):
    def __init__(self, session: CachedSession, amount: int, api_key: str = None, user_id: str = None):
        self.session = session
        self.amount: int = amount

        if api_key or user_id:
            self.api_key = api_key
            self.user_id = user_id
            self.specs = {"api_key": self.api_key, "user_id": self.user_id}
        else:
            self.specs = {}

        self.data: str | None = None
        self.final: dict | None = None
        self.query: str | None = None

    async def _search(
        self,
        url: str,
        query: str,
        block: str = "",
        limit: int = 100,
        page: int = randint(0, 100),
        gacha: bool = False,
    ) -> dict | None:
        if gacha:
            limit = 100

        if limit > 1000:
            raise ValueError(Booru.error_handling_limit)

        if block and re.findall(block, query):
            raise ValueError(Booru.error_handling_sameval)

        self.query = f"{query} -{block}*" if block != "" else query
        self.specs["tags"] = str(self.query)
        self.specs["limit"] = str(limit)
        self.specs["pid"] = page
        self.specs["json"] = "1"
        self.final = {"teste": 1}
        start_time = time.time()
        seconds = 12

        while self.final == {"teste": 1}:
            elapsed_time = time.time() - start_time
            if elapsed_time > seconds:
                return None
            self.response = await self.session.get(url, params=self.specs, allow_redirects=True)
            self.data = await self.response.text()
            try:
                self.final = json.loads(self.data)
            except Exception as e:
                return None
            if self.final in [
                {"@attributes": {"count": 0, "limit": 100, "offset": 0}},
                {"@attributes": {"count": 1, "limit": 100, "offset": 0}},
            ]:
                self.final = {"teste": 1}
            self.specs["pid"] = randint(0, 5)

        if not self.final:
            raise ValueError(Booru.error_handling_null)

        return self.final


class SearchDictType2(object):
    def __init__(self, session: CachedSession, amount: int, api_key: str = None, user_id: str = None):
        self.session = session
        self.amount: int = amount

        if api_key or user_id:
            self.api_key = api_key
            self.user_id = user_id
            self.specs = {"api_key": self.api_key, "user_id": self.user_id}
        else:
            self.specs = {}

        self.data: str | None = None
        self.final: dict | None = None
        self.query: str | None = None

    async def _search(
        self,
        url: str,
        query: str,
        block: str = "",
        limit: int = 100,
        page: int = randint(0, 100),
        gacha: bool = False,
    ) -> dict | None:
        if gacha:
            limit = 100

        if limit > 1000:
            raise ValueError(Booru.error_handling_limit)

        if block and re.findall(block, query):
            raise ValueError(Booru.error_handling_sameval)

        self.specs["q"] = str(query)
        self.specs["per_page"] = str(limit)
        self.specs["page"] = page
        self.final = {"teste": 1}
        start_time = time.time()
        seconds = 12

        while self.final == {"teste": 1}:
            elapsed_time = time.time() - start_time
            if elapsed_time > seconds:
                return None
            self.response = await self.session.get(url, params=self.specs, allow_redirects=True)
            self.data = await self.response.text()
            try:
                self.final = json.loads(self.data)
            except Exception as e:
                return None
            if self.final["total"] == 0 or len(self.final['images']) == 0:
                self.final = {"teste": 1}
            self.specs["page"] = randint(0, 5)

        if not self.final:
            raise ValueError(Booru.error_handling_null)

        return self.final
