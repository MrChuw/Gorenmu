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


class UploadThings:
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot

    @staticmethod
    async def pastbin_upload(text: str, bot: Gorenmu, cache: SQLiteBackend):
        await asyncio.sleep(0)
        async with CachedSession(cache=cache) as session:
            async with session.post(bot.config.BotConfig.pastbin_url, data=text.encode("utf-8")) as r:
                if r.status != 200:
                    return None
                return (await r.read()).decode("utf8")

    @staticmethod
    async def send_imgur(links: list[str], bot: Gorenmu, session: CachedSession):
        try:
            session.headers.update({"x-api-key": bot.config.ApisConfig.image_carousel_api_key})
            response = await session.post(bot.config.ApisConfig.image_carousel, json={"urls": links})
            embed = json.loads(await response.text())
            session.headers.pop('x-api-key')
            return embed["success"]
        except Exception as e:
            logger.error(e)
            return None

    @staticmethod
    async def shortener(url: str | None, tags: list[str], bot: Gorenmu, session: CachedSession):
        shlink_url = bot.config.ApisConfig.shlink_url
        payload = {"longUrl": url, "forwardQuery": "true", "findIfExists": "true", "tags": tags}
        headers = {
                "accept": "application/json",
                "Content-Type": "application/json",
                "X-Api-Key": bot.config.ApisConfig.shlink_key}
        if url is None:
            return None
        try:
            response = await session.post(shlink_url, json=payload, headers=headers)
            response = await response.json()
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

                async with session.post(bot.config.BotConfig.file_upload_url, data=body, headers=headers) as resp:
                    return json.loads(await resp.text())

        except Exception as e:
            logger.error(e)
            return None
