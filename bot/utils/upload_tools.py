from __future__ import annotations

from typing import TYPE_CHECKING

from loguru import logger

from bot.utils.singleton import Singleton

if TYPE_CHECKING:
    from aiohttp_client_cache import CachedSession

    from bot.bot import Gorenmu


class UploadThings(metaclass=Singleton):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot

    @staticmethod
    async def _safe_post(session: CachedSession, url: str, **kwargs):
        try:
            response = await session.post(url, **kwargs)
            if response.status in [200, 201]:
                return response
            logger.warning(f"Request to {url} failed with status {response.status}")
        except Exception as e:
            logger.exception(f"Error posting to {url}: {e}")
        return None

    async def _bytes_post(self, session: CachedSession, url: str, **kwargs) -> str:
        response = await self._safe_post(session, url, **kwargs)
        return (await response.read()).decode("utf-8") if response else None

    async def _json_post(self, session: CachedSession, url: str, **kwargs) -> dict:
        response = await self._safe_post(session, url, **kwargs)
        return await response.json() if response else None

    async def pastebin_upload(self, text: str, session: CachedSession):
        response = await self._json_post(session, self.bot.config.ApisConfig.pastebin_url, data=text.encode("utf-8"))
        if "key" in response:
            return self.bot.config.ApisConfig.pastebin_url.parent / response["key"]
        return None

    async def send_imgur(self, links: list[str], session: CachedSession):
        url = self.bot.config.ApisConfig.image_carousel
        headers = {"x-api-key": self.bot.config.ApisConfig.image_carousel_api_key}
        data = await self._json_post(session, url, json={"urls": links}, headers=headers)
        session.headers.pop("x-api-key", None)
        if data:
            try:
                return data.get("success")
            except Exception as e:
                logger.error(f"Failed to parse Imgur response: {e}")
        return None

    async def shortener(self, url: str | None, tags: list[str], session: CachedSession):
        if url is None:
            return None
        tags += ["Gorenmu"]
        shlink_url = self.bot.config.ApisConfig.shlink_url
        payload = {
            "longUrl": url,
            "forwardQuery": "true",
            "findIfExists": "true",
            "tags": tags,
        }
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "X-Api-Key": self.bot.config.ApisConfig.shlink_key,
        }
        data = await self._json_post(session, shlink_url, json=payload, headers=headers)
        session.headers.pop("x-api-key", None)
        if data:
            try:
                return None if "status" in data else data.get("shortUrl")
            except Exception as e:
                logger.error(f"Failed to parse shortener response: {e}")
        return None

    async def upload_file(
        self,
        data: bytes,
        mime_type: str,
        filename: str,
        session: CachedSession,
        url: str,
        api_key: dict[str, str],
    ) -> str | None:
        boundary = "faa88938ece74999ac092a3e782951fb"
        url = url
        headers = {"Content-Type": f"multipart/form-data; boundary={boundary}"} | api_key
        body = (
            (
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
                f"Content-Type: {mime_type}\r\n\r\n"
            ).encode()
            + data
            + f"\r\n--{boundary}--\r\n".encode()
        )

        data = await self._json_post(session, url, data=body, headers=headers)
        session.headers.pop("x-api-key", None)
        if "url" in data:
            return data["url"]
        elif "message" in data:
            return data["message"]
        return None

    async def upload_alias(self, data: dict, session: CachedSession):
        url = self.bot.config.ApisConfig.alias_url
        response = await self._safe_post(session, url, data=data)
        return response.url.human_repr() if response else None
