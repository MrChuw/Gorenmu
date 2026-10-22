from __future__ import annotations

import json as json_out
from datetime import datetime
from typing import TYPE_CHECKING, Any, Literal, Protocol, TypeVar, overload, runtime_checkable

from aiohttp import ClientResponse
from yarl import URL

from bot.utils.singleton import Singleton

from .parsers import (
    APIZonian,
    ChannelMessages,
    Channels,
    ChannelStats,
    ChannelsZonian,
    Health,
    Instances,
    List,
    NameHistory,
    Random,
    Search,
    Stats,
)

if TYPE_CHECKING:
    from aiohttp_client_cache import CachedSession

    from bot.bot import Context, Gorenmu

ParsableType = (
    type[Channels]
    | type[List]
    | type[NameHistory]
    | type[Search]
    | type[Stats]
    | type[ChannelStats]
    | type[Random]
    | type[ChannelMessages]
    | type[Instances]
    | type[ChannelsZonian]
    | type[Health]
)

T = TypeVar("T")


@runtime_checkable
class Parsable(Protocol):
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Any: ...


@runtime_checkable
class ParsableAlt(Protocol):
    @classmethod
    def from_dict_alt(cls, data: dict[str, Any]) -> Any: ...


class Base:
    def __init__(self, bot: Gorenmu, session: CachedSession, url: URL):
        self.bot = bot
        self.session = session
        self.base_url: URL = url


class BestLogs(metaclass=Singleton):
    def __init__(self, bot: Gorenmu, session: CachedSession):
        self.bot = bot
        self.session: CachedSession = session
        self.base_url: URL = bot.config.ApisConfig.best_logs
        self.RustLogs: RustLogs = RustLogs(bot=bot, session=session, base_url=self.base_url)
        self.ZonianLogs: ZonianLogs = ZonianLogs(bot=bot, session=session, base_url=self.base_url)


class RustLogs(Base):
    def __init__(self, bot: Gorenmu, session: CachedSession, base_url: URL):
        self.bot = bot
        self.session: CachedSession = session
        self.base_url: URL = base_url

        for name, cls in vars(self.__class__).items():
            if isinstance(cls, type) and issubclass(cls, Base):
                setattr(self, name, cls(bot, self.session, self.base_url))
        super().__init__(bot, session, self.base_url)

    async def get_channels(self, ctx: Context):
        response = await self.session.get(self.base_url / "channels")
        return await try_parse(self.bot, ctx, Channels, response)

    async def get_list(
        self, ctx: Context, channel: str | int, user: str | int | None = None
    ) -> str | List | str | None:
        url = self.base_url / "list"
        if str(channel).isnumeric():
            url = url.update_query(channelid=str(channel))
        elif isinstance(channel, str):
            url = url.update_query(channel=channel)
        else:
            raise raise_channel()
        if user is not None:
            if str(user).isnumeric():
                url = url.update_query(userid=str(user))
            elif isinstance(user, str):
                url = url.update_query(user=user)
            else:
                raise raise_user()
        response = await self.session.get(url)
        return await try_parse(self.bot, ctx, List, response)

    async def name_history(self, ctx: Context, user: str | int) -> str | list[NameHistory] | str | None:
        url = self.base_url / "namehistory"
        if str(user).isnumeric():
            url = url / "userid" / str(user)
        elif isinstance(user, str):
            url = url / "user" / str(user)
        else:
            raise raise_user()

        response = await self.session.get(url)
        return await try_parse(self.bot, ctx, NameHistory, response, alt=True)

    async def search(
        self,
        ctx: Context,
        channel: str | int,
        user: str | int,
        *,
        json: bool = True,
        json_basic: bool = False,
        raw: bool = False,
        reverse: bool = False,
        ndjson: bool = False,
        limit: int | None = None,
        offset: int | None = None,
    ) -> str | Search | str | None:
        if str(channel).isnumeric():
            url = self.base_url / "channelid" / str(channel)
        elif isinstance(channel, str):
            url = self.base_url / "channel" / str(channel)
        else:
            raise raise_channel()

        if str(user).isnumeric():
            url = url / "userid" / str(user)
        elif isinstance(user, str):
            url = url / "user" / str(user)
        else:
            raise raise_user()

        url = url / "search"

        params = {
            "json": "true" if json else None,
            "jsonBasic": "true" if json_basic else None,
            "raw": "true" if raw else None,
            "reverse": "true" if reverse else None,
            "ndjson": "true" if ndjson else None,
            "limit": limit,
            "offset": offset,
        }
        params = {k: v for k, v in params.items() if v is not None}

        response = await self.session.get(url, params=params | {"q": ""})

        if raw or ndjson or not json:
            return await response.text()

        response = await self.session.get(url, params=params)
        return await try_parse(self.bot, ctx, Search, response)

    async def get_user_stats(
        self,
        ctx: Context,
        channel: str | int,
        user: str | int,
        *,
        from_: datetime | None = None,
        to: datetime | None = None,
    ) -> str | Stats | None:
        if str(channel).isnumeric():
            url = self.base_url / "channelid" / str(channel)
        elif isinstance(channel, str):
            url = self.base_url / "channel" / str(channel)
        else:
            raise raise_channel()

        if str(user).isnumeric():
            url = url / "userid" / str(user)
        elif isinstance(user, str):
            url = url / "user" / str(user)
        else:
            raise raise_user()

        url = url / "stats"

        params = {}
        if from_:
            params["from"] = from_.strftime("%Y-%m-%dT%H:%M:%SZ")
        if to:
            params["to"] = to.strftime("%Y-%m-%dT%H:%M:%SZ")

        response = await self.session.get(url, params=params)
        return await try_parse(self.bot, ctx, Stats, response)

    async def get_channel_stats(
        self,
        ctx: Context,
        channel: str | int,
        *,
        from_: datetime | None = None,
        to: datetime | None = None,
    ) -> str | ChannelStats | None:
        if str(channel).isnumeric():
            url = self.base_url / "channelid" / str(channel)
        elif isinstance(channel, str):
            url = self.base_url / "channel" / str(channel)
        else:
            raise raise_channel()

        params = {}
        if from_:
            params["from"] = from_.strftime("%Y-%m-%dT%H:%M:%SZ")
        if to:
            params["to"] = to.strftime("%Y-%m-%dT%H:%M:%SZ")

        response = await self.session.get(url, params=params)
        return await try_parse(self.bot, ctx, ChannelStats, response)

    @overload
    async def get_random_message(
        self,
        ctx: Context,
        channel: str | int,
        user: str | int | None = ...,
        *,
        random: Literal[True],
        json: bool = ...,
        json_basic: bool = ...,
        raw: bool = ...,
        reverse: bool = ...,
        ndjson: bool = ...,
        limit: int | None = ...,
        offset: int | None = ...,
    ) -> Random | None: ...

    @overload
    async def get_random_message(
        self,
        ctx: Context,
        channel: str | int,
        user: str | int | None = ...,
        *,
        random: Literal[False],
        json: bool = ...,
        json_basic: bool = ...,
        raw: bool = ...,
        reverse: bool = ...,
        ndjson: bool = ...,
        limit: int | None = ...,
        offset: int | None = ...,
    ) -> str | None: ...

    @overload
    async def get_random_message(
        self,
        ctx: Context,
        channel: str | int,
        user: str | int | None = ...,
        *,
        random: bool = ...,
        json: bool = ...,
        json_basic: bool = ...,
        raw: bool = ...,
        reverse: bool = ...,
        ndjson: bool = ...,
        limit: int | None = ...,
        offset: int | None = ...,
    ) -> str | Random | None: ...

    async def get_random_message(
        self,
        ctx: Context,
        channel: str | int,
        user: str | int | None = None,
        *,
        random: bool = True,  # NOQA
        json: bool = True,
        json_basic: bool = False,
        raw: bool = False,
        reverse: bool = False,
        ndjson: bool = False,
        limit: int | None = None,
        offset: int | None = None,
    ) -> str | Random | None:
        if str(channel).isnumeric():
            url = self.base_url / "channelid" / str(channel)
        elif isinstance(channel, str):
            url = self.base_url / "channel" / str(channel)
        else:
            raise raise_channel()

        final_url = url / "random"

        if user is not None:
            if str(user).isnumeric():
                url = url / "userid" / str(user)
            elif isinstance(user, str):
                url = url / "user" / str(user)
            else:
                raise raise_user()
            final_url = url / "random"

        params = {
            "json": "true" if json else None,
            "jsonBasic": "true" if json_basic else None,
            "raw": "true" if raw else None,
            "reverse": "true" if reverse else None,
            "ndjson": "true" if ndjson else None,
            "limit": limit,
            "offset": offset,
        }
        params = {k: v for k, v in params.items() if v is not None}

        response = await self.session.get(final_url, params=params)

        if raw or ndjson or not json:
            return await response.text()

        return await try_parse(self.bot, ctx, Random, response)

    async def get_channel_messages(
        self,
        ctx: Context,
        channel: str | int,
        *,
        from_: datetime | None = None,
        to: datetime | None = None,
        json: bool = True,
        json_basic: bool = False,
        raw: bool = False,
        reverse: bool = False,
        ndjson: bool = False,
        limit: int | None = None,
        offset: int | None = None,
    ) -> str | ChannelMessages | None:
        if str(channel).isnumeric():
            url = self.base_url / "channelid" / str(channel)
        elif isinstance(channel, str):
            url = self.base_url / "channel" / str(channel)
        else:
            raise raise_channel()

        params = {
            "from": from_.strftime("%Y-%m-%dT%H:%M:%SZ") if from_ else None,
            "to": to.strftime("%Y-%m-%dT%H:%M:%SZ") if to else None,
            "json": "true" if json else None,
            "jsonBasic": "true" if json_basic else None,
            "raw": "true" if raw else None,
            "reverse": "true" if reverse else None,
            "ndjson": "true" if ndjson else None,
            "limit": limit,
            "offset": offset,
        }
        params = {k: v for k, v in params.items() if v is not None}

        response = await self.session.get(url, params=params)
        if raw or ndjson or not json:
            return await response.text()

        return await try_parse(self.bot, ctx, ChannelMessages, response)

    async def get_user_messages(
        self,
        ctx: Context,
        channel: str | int,
        user: str | int,
        *,
        from_: datetime | None = None,
        to: datetime | None = None,
        json: bool = True,
        json_basic: bool = False,
        raw: bool = False,
        reverse: bool = False,
        ndjson: bool = False,
        limit: int | None = None,
        offset: int | None = None,
    ) -> str | ChannelMessages | None:
        if str(channel).isnumeric():
            url = self.base_url / "channelid" / str(channel)
        elif isinstance(channel, str):
            url = self.base_url / "channel" / str(channel)
        else:
            raise raise_channel()

        if str(user).isnumeric():
            url = url / "userid" / str(user)
        elif isinstance(user, str):
            url = url / "user" / str(user)
        else:
            raise raise_user()

        params = {
            "from": from_.strftime("%Y-%m-%dT%H:%M:%SZ") if from_ else None,
            "to": to.strftime("%Y-%m-%dT%H:%M:%SZ") if to else None,
            "json": "true" if json else None,
            "jsonBasic": "true" if json_basic else None,
            "raw": "true" if raw else None,
            "reverse": "true" if reverse else None,
            "ndjson": "true" if ndjson else None,
            "limit": limit,
            "offset": offset,
        }
        params = {k: v for k, v in params.items() if v is not None}

        response = await self.session.get(url, params=params)

        if raw or ndjson or not json:
            return await response.text()
        return await try_parse(self.bot, ctx, ChannelMessages, response)

    async def get_channel_messages_by_date(
        self,
        ctx: Context,
        channel: str | int,
        year: int,
        month: int,
        day: int,
        *,
        json: bool = True,
        json_basic: bool = False,
        raw: bool = False,
        reverse: bool = False,
        ndjson: bool = False,
        limit: int | None = None,
        offset: int | None = None,
    ) -> str | ChannelMessages | None:
        if str(channel).isnumeric():
            url = self.base_url / "channelid" / str(channel) / str(year) / f"{month:02d}" / f"{day:02d}"
        elif isinstance(channel, str):
            url = self.base_url / "channel" / str(channel) / str(year) / f"{month:02d}" / f"{day:02d}"
        else:
            raise raise_channel()

        params = {
            "json": "true" if json else None,
            "jsonBasic": "true" if json_basic else None,
            "raw": "true" if raw else None,
            "reverse": "true" if reverse else None,
            "ndjson": "true" if ndjson else None,
            "limit": limit,
            "offset": offset,
        }
        params = {k: v for k, v in params.items() if v is not None}

        response = await self.session.get(url, params=params)

        if raw or ndjson or not json:
            return await response.text()
        return await try_parse(self.bot, ctx, ChannelMessages, response)

    async def get_user_messages_by_month(
        self,
        ctx: Context,
        channel: str | int,
        user: str | int,
        year: int,
        month: int,
        *,
        json: bool = True,
        json_basic: bool = False,
        raw: bool = False,
        reverse: bool = False,
        ndjson: bool = False,
        limit: int | None = None,
        offset: int | None = None,
    ) -> str | ChannelMessages | None:
        if str(channel).isnumeric():
            base = self.base_url / "channelid" / str(channel)
        elif isinstance(channel, str):
            base = self.base_url / "channel" / str(channel)
        else:
            raise raise_channel()

        if str(user).isnumeric():
            base = base / "userid" / str(user)
        elif isinstance(user, str):
            base = base / "user" / str(user)
        else:
            raise raise_user()

        url = base / str(year) / f"{month:02d}"

        params = {
            "json": "true" if json else None,
            "jsonBasic": "true" if json_basic else None,
            "raw": "true" if raw else None,
            "reverse": "true" if reverse else None,
            "ndjson": "true" if ndjson else None,
            "limit": limit,
            "offset": offset,
        }
        params = {k: v for k, v in params.items() if v is not None}

        response = await self.session.get(url, params=params)

        if raw or ndjson or not json:
            return await response.text()
        return await try_parse(self.bot, ctx, ChannelMessages, response)


class ZonianLogs(Base):
    def __init__(self, bot: Gorenmu, session: CachedSession, base_url: URL):
        self.bot = bot
        self.session: CachedSession = session
        self.base_url: URL = base_url

        for name, cls in vars(self.__class__).items():
            if isinstance(cls, type) and issubclass(cls, Base):
                setattr(self, name, cls(bot, self.session, self.base_url))
        super().__init__(bot, session, self.base_url)

    async def api(
        self, ctx: Context, channel: str | int, user: str | int | None = None
    ) -> str | APIZonian | str | None:
        if str(channel).isnumeric():
            url = self.base_url / "api" / f"id:{channel}"
        elif isinstance(channel, str):
            url = self.base_url / "api" / channel
        else:
            raise raise_channel()

        if user:
            if str(user).isnumeric():
                url = url / f"id{user!s}"
            elif isinstance(user, str):
                url = url / str(user)
            else:
                raise raise_user()

        response = await self.session.get(url)
        return await try_parse(self.bot, ctx, APIZonian, response)

    async def redirect(self, channel: str | int, user: str | int | None = None) -> str | None:
        if str(channel).isnumeric():
            url = self.base_url / "rdr" / f"id:{channel}"
        elif isinstance(channel, str):
            url = self.base_url / "rdr" / channel
        else:
            raise raise_channel()

        if user:
            if str(user).isnumeric():
                url = url / f"id{user!s}"
            elif isinstance(user, str):
                url = url / str(user)
            else:
                raise raise_user()

        response = await self.session.get(url)
        return await response.text()

    async def name_history(self, ctx: Context, user: str | int) -> str | list[NameHistory] | None:
        if str(user).isnumeric():
            url = self.base_url / "namehistory" / str(user)
        elif isinstance(user, str):
            url = self.base_url / "namehistory" / f"login:{user}"
        else:
            raise raise_user()

        response = await self.session.get(url)
        return await try_parse(self.bot, ctx, NameHistory, response, alt=True)

    async def instances(self, ctx: Context) -> str | Instances | str | None:
        response = await self.session.get(self.base_url / "instances")
        return await try_parse(self.bot, ctx, Instances, response)

    async def channels(self, ctx: Context) -> str | ChannelsZonian | str | None:
        response = await self.session.get(self.base_url / "channels")
        return await try_parse(self.bot, ctx, ChannelsZonian, response)

    async def health(self, ctx: Context) -> str | Health | str | None:
        response = await self.session.get(self.base_url / "health")
        return await try_parse(self.bot, ctx, Health, response)


def raise_channel():
    return TypeError("User must be a string (channel) or integer (channel ID).")


def raise_channel_str():
    return TypeError("User must be a string (channel) or integer (channel ID).")


def raise_user():
    return TypeError("User must be a string (username) or integer (user ID).")


@overload
async def try_parse(
    bot: Gorenmu,
    ctx: Context,
    cls: type[T],
    response: ClientResponse,
    alt: Literal[True],
) -> list[T] | str | None: ...


@overload
async def try_parse(
    bot: Gorenmu,
    ctx: Context,
    cls: type[T],
    response: ClientResponse,
    alt: Literal[False] = False,
) -> T | str | None: ...


async def try_parse(
    bot: Gorenmu,
    ctx: Context,
    cls: type[T],
    response: ClientResponse,
    alt: bool = False,
) -> T | list[T] | str | None:
    try:
        try:
            json_response = await response.json()
        except Exception:  # noqa
            json_response = json_out.loads(await response.text())

        if not json_response:
            return None

        if alt and hasattr(cls, "from_dict_alt"):  # noqa: SIM108
            parser = getattr(cls, "from_dict_alt")  # noqa: B009
        else:
            parser = getattr(cls, "from_dict")  # noqa: B009

        return parser(json_response)

    except Exception as e:
        await bot.CommandHandler.send_bug(ctx, e, ping=False)
        return await response.text()
