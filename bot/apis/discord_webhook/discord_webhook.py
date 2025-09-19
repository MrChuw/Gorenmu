# -*- coding: utf-8 -*-
from __future__ import annotations

import asyncio
import json
import logging
import secrets
from datetime import datetime, timezone
from functools import partial
from http.client import HTTPException
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union

if TYPE_CHECKING:
    import aiohttp
    from aiohttp_client_cache import CachedSession

    # from contextlib import asynccontextmanager

# Original code in https://github.com/lovvskillz/python-discord-webhook/

logger = logging.getLogger(__name__)


class ColorNotInRangeException(Exception):
    def __init__(self, color: Union[str, int], message=None) -> None:
        if not message:
            message = (
                f"{color!r} is not in valid range of colors. The valid ranges of colors"
                " are 0 to 16777215 inclusive (INTEGERS) and 0 to FFFFFF inclusive"
                " (HEXADECIMAL)."
            )
        super().__init__(message)


class DiscordEmbed:
    """
    Discord Embed
    """

    author: Optional[Dict[str, Optional[str]]]
    color: Optional[int]
    description: Optional[str]
    fields: List[Dict[str, Optional[Any]]]
    footer: Optional[Dict[str, Optional[str]]]
    image: Optional[Dict[str, Optional[Union[str, int]]]]
    provider: Optional[Dict[str, Any]]
    thumbnail: Optional[Dict[str, Optional[Union[str, int]]]]
    timestamp: Optional[str]
    title: Optional[str]
    url: Optional[str]
    video: Optional[Dict[str, Optional[Union[str, int]]]]

    def __init__(self, title: Optional[str] = None, description: Optional[str] = None, **kwargs: Any) -> None:
        """
        Init Discord Embed
        -----------
        :keyword dict author: information about the author
        :keyword color: color code of the embed as decimal or hexadecimal
        :keyword str description: description of the embed
        :keyword list fields: embed fields as a list of dicts with name and value
        :keyword dict footer: information that will be displayed in the footer
        :keyword dict image: image that will be displayed in the embed
        :keyword dict provider: information about the provider
        :keyword dict thumbnail: thumbnail that will be displayed in the embed
        :keyword float, int, str, datetime timestamp: timestamp that will be displayed in the embed
        :keyword str title: title of embed
        :keyword str url: add an url to make your embedded title a clickable link
        :keyword dict video: video that will be displayed in the embed
        """
        self.title = title
        self.description = description
        self.url = kwargs.get("url")
        self.footer = kwargs.get("footer")
        self.image = kwargs.get("image")
        self.thumbnail = kwargs.get("thumbnail")
        self.video = kwargs.get("video")
        self.provider = kwargs.get("provider")
        self.author = kwargs.get("author")
        self.fields = kwargs.get("fields", [])
        self.set_color(kwargs.get("color"))
        if timestamp := kwargs.get("timestamp"):
            self.set_timestamp(timestamp)

    def set_title(self, title: str) -> None:
        """
        Set the title of the embed.
        :param str title: title of embed
        """
        self.title = title

    def set_description(self, description: str) -> None:
        """
        Set the description of the embed.
        :param str description: description of embed
        """
        self.description = description

    def set_url(self, url: str) -> None:
        """
        Set the url of the embed.
        :param str url: url of embed
        """
        self.url = url

    def set_timestamp(self, timestamp: Optional[Union[float, int, str, datetime]] = None) -> None:
        """
        Set timestamp of the embed content.
        :param timestamp: optional timestamp of embed content
        """
        if timestamp is None:
            timestamp = datetime.now(timezone.utc)
        elif isinstance(timestamp, float) or isinstance(timestamp, int):
            timestamp = datetime.fromtimestamp(timestamp, timezone.utc).replace(tzinfo=None)

        if not isinstance(timestamp, str):
            timestamp = timestamp.isoformat()

        self.timestamp = timestamp

    def set_color(self, color: Union[str, int]) -> None:
        """
        Set the color of the embed.
        :param color: color code as decimal(int) or hex(string)
        """
        self.color = int(color, 16) if isinstance(color, str) else color
        if self.color is not None and self.color not in range(16777216):
            raise ColorNotInRangeException(color)

    def set_footer(self, text: str, **kwargs) -> None:
        """
        Set footer information in the embed.
        :param str text: footer text
        :keyword str icon_url: url of footer icon (only http(s) and attachments)
        :keyword str proxy_icon_url: proxied url of footer icon
        """
        self.footer = {"text": text, "icon_url": kwargs.get("icon_url"), "proxy_icon_url": kwargs.get("proxy_icon_url")}

    def set_image(self, url: str, **kwargs: Union[str, int]) -> None:
        """
        Set the image that will be displayed in the embed.
        :param str url: source url of image (only supports http(s) and attachments)
        :keyword str proxy_url: a proxied url of the image
        :keyword int height: height of image
        :keyword int width: width of image
        """
        self.image = {
            "url": url,
            "proxy_url": kwargs.get("proxy_url"),
            "height": kwargs.get("height"),
            "width": kwargs.get("width"),
        }

    def set_thumbnail(self, url: str, **kwargs: Union[str, int]) -> None:
        """
        Set the thumbnail that will be displayed in the embed.
        :param str url: source url of thumbnail (only supports http(s) and attachments)
        :keyword str proxy_url: a proxied thumbnail of the image
        :keyword int height: height of thumbnail
        :keyword int width: width of thumbnail
        """
        self.thumbnail = {
            "url": url,
            "proxy_url": kwargs.get("proxy_url"),
            "height": kwargs.get("height"),
            "width": kwargs.get("width"),
        }

    def set_video(self, **kwargs: Union[str, int]) -> None:
        """
        Set the video that will be displayed in the embed.
        :keyword str url: source url of video
        :keyword int height: height of video
        :keyword int width: width of video
        """
        self.video = {"url": kwargs.get("url"), "height": kwargs.get("height"), "width": kwargs.get("width")}

    def set_provider(self, **kwargs: str) -> None:
        """
        Set the provider information of the embed.
        :keyword str name: name of provider
        :keyword str url: url of provider
        """
        self.provider = {"name": kwargs.get("name"), "url": kwargs.get("url")}

    def set_author(self, name: str, **kwargs: str) -> None:
        """
        Set information about the author of the embed.
        :param name: name of author
        :keyword url: url of author
        :keyword icon_url: url of author icon (only supports http(s) and
        attachments)
        :keyword proxy_icon_url: a proxied url of author icon
        """
        self.author = {
            "name": name,
            "url": kwargs.get("url"),
            "icon_url": kwargs.get("icon_url"),
            "proxy_icon_url": kwargs.get("proxy_icon_url"),
        }

    def add_embed_field(self, name: str, value: str, inline: bool = True) -> None:
        """
        Set a field with information for the embed
        :param str name: name of the field
        :param str value: value of the field
        :param bool inline: (optional) whether this field should display inline
        """
        self.fields.append({"name": name, "value": value, "inline": inline})

    def delete_embed_field(self, index: int) -> None:
        """
        Remove a field from the already stored embed fields.
        :param int index: index of field in `self.fields`
        """
        self.fields.pop(index)

    def get_embed_fields(self) -> List[Dict[str, Optional[Any]]]:
        """
        Get all stored fields of the embed as a list.
        :return: fields of the embed
        """
        return self.fields


class DiscordWebhook:
    def __init__(self, url: str, session: CachedSession, **kwargs) -> None:
        """
        Init Webhook for Discord.
        ---------
        :param str url: your discord webhook url
        :keyword dict allowed_mentions: allowed mentions for the message
        :keyword dict attachments: attachments that should be included
        :keyword str avatar_url: override the default avatar of the webhook
        :keyword str content: the message contents
        :keyword list embeds: list of embedded rich content
        :keyword int flags: apply flags to the message
        :keyword dict files: to apply file(s) with message
        :keyword str id: webhook id
        :keyword dict proxies: proxies that should be used
        :keyword bool rate_limit_retry: whether the message should be sent again when being rate limited
        :keyword str thread_id: send message to a thread specified by its thread id
        :keyword str thread_name: name of thread to create
        :keyword int timeout: seconds to wait for a response from Discord
        :keyword bool tts: indicates if this is a TTS message
        :keyword str username: override the default username of the webhook
        :keyword bool wait: waits for server confirmation of message send before response (defaults to True)
        """
        self.url: str = url
        self.session: CachedSession = session
        self.flags = kwargs.get("flags")
        self.components: Optional[list] = []
        self.allowed_mentions: Dict[str, List[str]] = kwargs.get("allowed_mentions", {})
        self.attachments: Optional[List[Dict[str, Any]]] = kwargs.get("attachments", [])
        self.avatar_url: Optional[str] = kwargs.get("avatar_url")
        self.content: Optional[Union[str, bytes]] = kwargs.get("content")
        self.embeds: List[Dict[str, Any]] = kwargs.get("embeds", [])
        self.files: Dict[str, Tuple[Optional[str], Union[bytes, str]]] = kwargs.get("files", {})
        self._files: List[Dict[str, str]] = []
        self.id: Optional[str] = kwargs.get("id")
        self.proxies: Optional[Dict[str, str]] = kwargs.get("proxies")
        self.rate_limit_retry: bool = kwargs.get("rate_limit_retry", False)
        self.thread_id: Optional[str] = kwargs.get("thread_id")
        self.thread_name: Optional[str] = kwargs.get("thread_name")
        self.timeout: Optional[float] = kwargs.get("timeout")
        self.tts: Optional[bool] = kwargs.get("tts", False)
        self.username: Optional[str] = kwargs.get("username", None)
        self.wait: Optional[bool] = kwargs.get("wait", True)

    def add_embed(self, embed: Union[DiscordEmbed, Dict[str, Any]]) -> None:
        """
        Add an embedded rich content.
        :param embed: embed object or dict.
        """
        self.embeds.append(embed.__dict__ if isinstance(embed, DiscordEmbed) else embed)

    def get_embeds(self) -> List[Dict[str, Any]]:
        """
        Get all embeds as a list.
        :return: embeds
        """
        return self.embeds

    def remove_embed(self, index: int) -> None:
        """
        Remove an embed from already added embeds to the webhook.
        :param int index: index of embed.
        """
        self.embeds.pop(index)

    def remove_embeds(self) -> None:
        """
        Remove all embeds.
        """
        self.embeds = []

    def add_file(self, file: bytes, filename: str) -> None:
        """
        Add a file to the webhook.
        :param bytes file: file content
        :param str filename: filename.
        """
        self.files[f"_{filename}"] = (filename, file)
        self._files.append({"field_name": filename, "content": file})

    def remove_file(self, filename: str) -> None:
        """
        Remove the file by the given filename if it exists.
        :param str filename: filename
        """
        self.files.pop(f"_{filename}", None)
        if self.attachments:
            index = next((i for i, item in enumerate(self.attachments) if item.get("filename") == filename), None)
            if index is not None:
                self.attachments.pop(index)

    def remove_files(self, clear_attachments: bool = True) -> None:
        """
        Remove all files and optionally clear the attachments.
        :param bool clear_attachments: Clear the attachments.
        """
        self.files = {}
        if clear_attachments:
            self.clear_attachments()

    def clear_attachments(self) -> None:
        """
        Remove all attachments.
        """
        self.attachments = []

    def set_proxies(self, proxies: Dict[str, str]) -> None:
        """
        Set proxies that should be used when sending the webhook.
        :param dict proxies: dict of proxies.
        """
        self.proxies = proxies

    def set_content(self, content: str) -> None:
        """
        Set the content of the webhook.
        :param str content: content of the webhook.
        """
        self.content = content

    def set_flags(self, flags: int) -> None:
        """
        Set the flags of the webhook.
        :param int flags: flags as integer.
        """
        self.flags = flags

    @property
    def json(self) -> Dict[str, Any]:
        """
        Convert data of the webhook to JSON.
        :return: webhook data as json.
        """
        embeds = self.embeds
        self.embeds = []
        # convert DiscordEmbed to dict
        for embed in embeds:
            self.add_embed(embed)
        data = {
            key: value
            for key, value in self.__dict__.items()
            if value and key not in ["url", "files"] or key in ["embeds", "attachments"]
        }
        embeds_empty = not any(data["embeds"]) if "embeds" in data else True
        if embeds_empty and "content" not in data and bool(self.files) is False:
            logger.error("webhook message is empty! set content or embed data")
        data.pop("session")
        return data

    # @property
    # @asynccontextmanager
    # async def http_client(self) -> "httpx.AsyncClient":
    #     """
    #     A property that returns a httpx.AsyncClient instance that is used for a 'with' statement.
    #     Example:
    #         async with self.client as client:
    #             client.post(url, data=data)
    #     It will automatically close the client when the context is exited.
    #     :return: httpx.AsyncClient
    #     """
    #     client = httpx.AsyncClient(proxy=self.proxies)
    #     yield client
    #     await client.aclose()

    @staticmethod
    def _make_multipart(
        files: List[Dict[str, Union[str, bytes]]], extra_headers: Dict[str, str] | None = None
    ) -> Tuple[bytes, Dict[str, str]]:
        """
        files: list[dict[str, str]] with:
            - field_name: field name
            - filename: file name, optional
            - content: content (bytes or str)
            - content_type: MIME type (default: application/octet-stream)
        """
        boundary = secrets.token_hex(16)
        boundary_bytes = boundary.encode()

        body = b""
        for f in files:
            field_name = f["field_name"]
            filename = f.get("filename")
            content = f["content"]
            if isinstance(content, str):
                content = content.encode()
            content_type = f.get("content_type", "application/octet-stream")

            body += b"--" + boundary_bytes + b"\r\n"

            if filename:
                body += (
                    f'Content-Disposition: form-data; name="{field_name}"; filename="{filename}"\r\n'.encode()
                    + f"Content-Type: {content_type}\r\n\r\n".encode()
                )
            else:
                body += f'Content-Disposition: form-data; name="{field_name}"\r\n\r\n'.encode()

            body += content + b"\r\n"

        body += b"--" + boundary_bytes + b"--\r\n"

        headers = {"Content-Type": f"multipart/form-data; boundary={boundary}"}

        if extra_headers:
            headers.update(extra_headers)

        return body, headers

    async def api_post_request(self) -> aiohttp.ClientResponse:
        """
        Post the JSON converted webhook data to the specified url.
        :return:
        """

        if not bool(self.files):
            response = await self.session.post(
                self.url, json=self.json, params=json.dumps(self._query_params), timeout=self.timeout
            )
        else:
            self.files["payload_json"] = (None, json.dumps(self.json).encode("utf-8"))
            body, headers = self._make_multipart(files=self._files)
            response = await self.session.post(
                self.url, data=body, headers=headers, params=json.dumps(self._query_params), timeout=self.timeout
            )
        return response

    @staticmethod
    async def handle_rate_limit(response: aiohttp.ClientResponse, request) -> aiohttp.ClientResponse | None:
        """
        Handle the rate limit by resending the webhook until a successful response.
        :param response: Response
        :param request: request function
        :return: Response of the send webhook.
        """
        while response.status == 429:
            errors = await response.json()
            if not response.headers.get("Via"):
                raise HTTPException(errors)
            wh_sleep = float(errors["retry_after"]) + 0.15
            logger.error("Webhook rate limited: sleeping for {wh_sleep} seconds...".format(wh_sleep=round(wh_sleep, 2)))
            await asyncio.sleep(wh_sleep)
            response: aiohttp.ClientResponse = await request()
            if response.status in [200, 204]:
                return response
        return None

    @property
    def _query_params(self) -> dict:
        """
        Set query parameters for requests.
        :return: Query parameters as dict
        """
        params = {}
        if self.thread_id:
            params["thread_id"] = self.thread_id
        if self.wait:
            params["wait"] = self.wait
        return params

    async def execute(self, remove_embeds=False) -> aiohttp.ClientResponse:
        """
        Execute the sending of the webhook with the given data.
        :param bool remove_embeds: clear the stored embeds after web hook is executed
        :return: Response of the send webhook.
        """
        response = await self.api_post_request()
        if response.status in [200, 204]:
            logger.debug("Webhook executed")
        elif response.status == 429 and self.rate_limit_retry:
            response = await self.handle_rate_limit(response, self.api_post_request)
        else:
            logger.error(
                "Webhook status code {status_code}: {content}".format(
                    status_code=response.status, content=await response.text("utf-8")
                )
            )
        if remove_embeds:
            self.remove_embeds()
        self.remove_files(clear_attachments=False)
        if response.status != 204:  # don't parse if response has no content (204 response code)
            if webhook_id := (await response.json(encoding="utf-8")).get("id"):
                self.id = webhook_id
        return response

    async def edit(self) -> aiohttp.ClientResponse:
        """
        Edit an already sent webhook with updated data.
        :return: Response of the send webhook.
        """
        assert isinstance(self.id, str), "Webhook ID needs to be set in order to edit the webhook."
        assert isinstance(self.url, str), "Webhook URL needs to be set in order to edit the webhook."
        url = f"{self.url}/messages/{self.id}"
        if not bool(self.files):
            patch_kwargs = {"json": self.json, "params": self._query_params, "timeout": self.timeout}
        else:
            self.files["payload_json"] = (None, json.dumps(self.json))
            body, headers = self._make_multipart(files=self._files)
            patch_kwargs = {"files": body, "headers": headers, "params": self._query_params, "timeout": self.timeout}
        request = partial(self.session.patch, url, **patch_kwargs)
        response = await request()  # NOQA
        if response.status_code in [200, 204]:
            logger.debug("Webhook with id {id} edited".format(id=self.id))
        elif response.status_code == 429 and self.rate_limit_retry:
            response = await self.handle_rate_limit(response, request)
            logger.debug("Webhook edited")
        else:
            logger.error(
                "Webhook status code {status_code}: {content}".format(
                    status_code=response.status_code, content=response.text("utf-8")
                )
            )
        return response

    async def delete(self) -> aiohttp.ClientResponse:
        """
        Delete the already sent webhook.
        :return: webhook response.
        """
        assert isinstance(self.id, str), "Webhook ID needs to be set in order to delete the webhook."
        assert isinstance(self.url, str), "Webhook URL needs to be set in order to delete the webhook."
        url = f"{self.url}/messages/{self.id}"
        response = await self.session.delete(url, params=self._query_params, timeout=self.timeout)
        if response.status in [200, 204]:
            logger.debug("Webhook deleted")
        else:
            logger.error(
                "Webhook status code {status_code}: {content}".format(
                    status_code=response.status, content=response.text("utf-8")
                )
            )
        return response

    @classmethod
    def create_batch(cls, urls: List[str], **kwargs) -> Tuple["DiscordWebhook", ...]:
        """
        Create a webhook instance for each specified URL.
        :param list urls: webhook URLs to be used for the instances
        :param kwargs: the same kwargs that are used for an instance of the class
        :return: tuple of webhook instances.
        """
        if "url" in kwargs:
            raise TypeError("'url' can't be used as a keyword argument.")
        return tuple([cls(url, **kwargs) for url in urls])
