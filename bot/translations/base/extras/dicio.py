# -*- coding: utf-8 -*-

import asyncio

import aiohttp
from aiohttp_client_cache import CachedSession, RedisBackend, SQLiteBackend
from bs4 import BeautifulSoup



class Dicio:
    def __init__(self):
        self.lock: asyncio.Lock = asyncio.Lock()

    @staticmethod
    async def request_word(palavra: str, cache: SQLiteBackend | RedisBackend) -> aiohttp.ClientResponse:
        ...

    @staticmethod
    async def page_title(request: aiohttp.ClientResponse):
        ...