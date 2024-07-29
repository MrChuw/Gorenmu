# -*- coding: utf-8 -*-
import html
from dataclasses import dataclass

import aiohttp


@dataclass
class Dictionary:
    url: str = "http://www.dicio.com.br"

    @classmethod
    async def exists(cls, word: str) -> bool:
        url = f"{cls.url}/{word}"
        response = await aiohttp.ClientSession().get(url)
        text = html.unescape(await response.text())
        start = text.find("<h1")
        if start != -1:
            start += len("<h1")
        start = text.find(">", start) + 1
        end = text.find("</h1>", start)
        find = text[start:end] if -1 < start < end else text
        find = find.split()[0]
        return find.lower() == word.lower()
