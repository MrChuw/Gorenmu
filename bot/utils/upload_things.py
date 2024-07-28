# -*- coding: utf-8 -*-
from __future__ import annotations

import asyncio
import json
from typing import TYPE_CHECKING

import aiohttp
from aiohttp_client_cache import CachedSession, SQLiteBackend
from loguru import logger

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class UploadThings:  # TODO: Arrumar as funções que estão aqui dentro.
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot

    @staticmethod
    async def pastbin_upload(text: str, cache: SQLiteBackend):
        await asyncio.sleep(0)
        async with CachedSession(cache=cache) as session:
            async with session.post("https://bin.mrchuw.com.br/documents", data=text.encode("utf-8")) as r:
                if r.status != 200:
                    return None
                return (await r.read()).decode("utf8")

    @staticmethod
    async def mandar_imgur(links: str, bot: Gorenmu, cache: SQLiteBackend):
        try:
            async with CachedSession(cache=cache, headers={"Authorization": bot.config.ApisConfig.site_api_key}
                                     ) as session:
                async with session.post("https://im.mrchuw.com.br/api/imgur/", json={"links": links}) as resp:
                    embed = json.loads(await resp.text())
                    return embed["url"]
        except Exception as e:
            logger.error(e)
            return None

    @staticmethod
    async def encurtar(url: str, bot: Gorenmu, cache: SQLiteBackend):
        timeout = aiohttp.ClientTimeout(total=20)
        shlink_url = bot.config.ApisConfig.shlink_url
        payload = {"longUrl": url, "forwardQuery": "true", "findIfExists": "true"}
        headers = {"accept": "application/json", "Content-Type": "application/json",
                   "X-Api-Key": bot.config.ApisConfig.shlink_key,
                   }
        if url is None:
            return None
        try:
            async with CachedSession(cache=cache, timeout=timeout) as session:
                async with session.post(shlink_url, json=payload, headers=headers) as resp:
                    response = json.loads(await resp.text())
                    resp.close()
                    if "status" in response:
                        return None
                    else:
                        return response["shortUrl"]
        except Exception as e:
            logger.error(e)
            return None

    @staticmethod
    async def upload(data: bytes, bot: Gorenmu, tipo: str, nome: str, cache: SQLiteBackend) -> dict | None:
        try:
            async with CachedSession(cache=cache) as session:
                body = (b"--faa88938ece74999ac092a3e782951fb\r\n"
                        b'Content-Disposition: form-data; name="files"; filename="' + nome.encode() + b'"\r\n' b"Content-Type:" + tipo.encode() + b"\r\n\r\n")
                body += data + b"\r\n"
                body += b"--faa88938ece74999ac092a3e782951fb--\r\n"

                headers = {"Content-Type": f"multipart/form-data; boundary=faa88938ece74999ac092a3e782951fb",
                           "Authorization": bot.config.ApisConfig.site_api_key,
                           }

                async with session.post("https://im.mrchuw.com.br/api/files/", data=body, headers=headers) as resp:
                    return json.loads(await resp.text())

        except Exception as e:
            logger.error(e)
            return None
