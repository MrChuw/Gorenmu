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
        url = "https://www.dicio.com.br/"
        async with CachedSession(cache=cache) as session:
            async with session.post(url + palavra) as resp:
                request = resp
        return request

    @staticmethod
    async def page_title(request: aiohttp.ClientResponse):
        soup = BeautifulSoup(await request.text(), "html.parser")
        title = soup.title.string if soup.title else "Título não encontrado"
        title = title.split(" ")[0]

        return title
