from dataclasses import dataclass
from typing import Any, TypeVar

from .shared import (
    from_bool,
    from_float,
    from_int,
    from_list,
    from_none,
    from_str,
    from_union,
    is_type,
    to_class,
    to_float,
)

T = TypeVar("T")


@dataclass
class Available:
    user: bool | None = None
    channel: bool | None = None

    @staticmethod
    def from_dict(obj: Any) -> "Available":
        assert isinstance(obj, dict)
        user = from_union([from_bool, from_none], obj.get("user"))
        channel = from_union([from_bool, from_none], obj.get("channel"))
        return Available(user, channel)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.user is not None:
            result["user"] = from_union([from_bool, from_none], self.user)
        if self.channel is not None:
            result["channel"] = from_union([from_bool, from_none], self.channel)
        return result


@dataclass
class Logs:
    count: int | None = None
    instances: list[str] | None = None
    full_link: list[str] | None = None

    @staticmethod
    def from_dict(obj: Any) -> "Logs":
        assert isinstance(obj, dict)
        count = from_union([from_int, from_none], obj.get("count"))
        instances = from_union([lambda x: from_list(from_str, x), from_none], obj.get("instances"))
        full_link = from_union([lambda x: from_list(from_str, x), from_none], obj.get("fullLink"))
        return Logs(count, instances, full_link)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.count is not None:
            result["count"] = from_union([from_int, from_none], self.count)
        if self.instances is not None:
            result["instances"] = from_union([lambda x: from_list(from_str, x), from_none], self.instances)
        if self.full_link is not None:
            result["fullLink"] = from_union([lambda x: from_list(from_str, x), from_none], self.full_link)
        return result


@dataclass
class Elapsed:
    ms: float | None = None
    s: float | None = None

    @staticmethod
    def from_dict(obj: Any) -> "Elapsed":
        assert isinstance(obj, dict)
        ms = from_union([from_float, from_none], obj.get("ms"))
        s = from_union([from_float, from_none], obj.get("s"))
        return Elapsed(ms, s)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.ms is not None:
            result["ms"] = from_union([to_float, from_none], self.ms)
        if self.s is not None:
            result["s"] = from_union([to_float, from_none], self.s)
        return result


@dataclass
class InstancesInfo:
    count: int | None = None
    down: int | None = None

    @staticmethod
    def from_dict(obj: Any) -> "InstancesInfo":
        assert isinstance(obj, dict)
        count = from_union([from_int, from_none], obj.get("count"))
        down = from_union([from_int, from_none], obj.get("down"))
        return InstancesInfo(count, down)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.count is not None:
            result["count"] = from_union([from_int, from_none], self.count)
        if self.down is not None:
            result["down"] = from_union([from_int, from_none], self.down)
        return result


@dataclass
class LastUpdated:
    unix: int | None = None
    utc: str | None = None

    @staticmethod
    def from_dict(obj: Any) -> "LastUpdated":
        assert isinstance(obj, dict)
        unix = from_union([from_int, from_none], obj.get("unix"))
        utc = from_union([from_str, from_none], obj.get("utc"))
        return LastUpdated(unix, utc)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.unix is not None:
            result["unix"] = from_union([from_int, from_none], self.unix)
        if self.utc is not None:
            result["utc"] = from_union([from_str, from_none], self.utc)
        return result


@dataclass
class Since:
    year: int | None = None
    month: int | None = None
    day: int | None = None

    @staticmethod
    def from_dict(obj: Any) -> "Since":
        assert isinstance(obj, dict)
        year = from_union([from_none, lambda x: int(from_str(x))], obj.get("year"))
        month = from_union([from_none, lambda x: int(from_str(x))], obj.get("month"))
        day = from_union([from_none, lambda x: int(from_str(x))], obj.get("day"))
        return Since(year, month, day)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.year is not None:
            result["year"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x)),
                ],
                self.year,
            )
        if self.month is not None:
            result["month"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x)),
                ],
                self.month,
            )
        if self.day is not None:
            result["day"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x)),
                ],
                self.day,
            )
        return result


@dataclass
class LoggedData:
    def __init__(self):
        self.list: list[Since] | None = None
        self.days: int | None = None
        self.since: Since | None = None

    @staticmethod
    def from_dict(obj: Any) -> "LoggedData":
        assert isinstance(obj, dict)
        _list = from_union([lambda x: from_list(Since.from_dict, x), from_none], obj.get("list"))
        days = from_union([from_int, from_none], obj.get("days"))
        since = from_union([Since.from_dict, from_none], obj.get("since"))
        return LoggedData(_list, days, since)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.list is not None:
            result["list"] = from_union(
                [lambda x: from_list(lambda x: to_class(Since, x), x), from_none],
                self.list,
            )
        if self.days is not None:
            result["days"] = from_union([from_int, from_none], self.days)
        if self.since is not None:
            result["since"] = from_union([lambda x: to_class(Since, x), from_none], self.since)
        return result


@dataclass
class OptedOut:
    count: int | None = None
    instances: list[Any] | None = None

    @staticmethod
    def from_dict(obj: Any) -> "OptedOut":
        assert isinstance(obj, dict)
        count = from_union([from_int, from_none], obj.get("count"))
        instances = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("instances"))
        return OptedOut(count, instances)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.count is not None:
            result["count"] = from_union([from_int, from_none], self.count)
        if self.instances is not None:
            result["instances"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.instances)
        return result


@dataclass
class Channel:
    login: str | None = None
    id: int | None = None
    banned: bool | None = None

    @staticmethod
    def from_dict(obj: Any) -> "Channel":
        assert isinstance(obj, dict)
        login = from_union([from_str, from_none], obj.get("login"))
        id = from_union([from_none, lambda x: int(from_str(x))], obj.get("id"))
        banned = from_union([from_bool, from_none], obj.get("banned"))
        return Channel(login, id, banned)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.login is not None:
            result["login"] = from_union([from_str, from_none], self.login)
        if self.id is not None:
            result["id"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x)),
                ],
                self.id,
            )
        if self.banned is not None:
            result["banned"] = from_union([from_bool, from_none], self.banned)
        return result


@dataclass
class Request:
    channel: Channel | None = None
    user: Channel | None = None
    forced: bool | None = None

    @staticmethod
    def from_dict(obj: Any) -> "Request":
        assert isinstance(obj, dict)
        channel = from_union([Channel.from_dict, from_none], obj.get("channel"))
        user = from_union([Channel.from_dict, from_none], obj.get("user"))
        forced = from_union([from_bool, from_none], obj.get("forced"))
        return Request(channel, user, forced)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.channel is not None:
            result["channel"] = from_union([lambda x: to_class(Channel, x), from_none], self.channel)
        if self.user is not None:
            result["user"] = from_union([lambda x: to_class(Channel, x), from_none], self.user)
        if self.forced is not None:
            result["forced"] = from_union([from_bool, from_none], self.forced)
        return result


@dataclass
class APIZonian:
    error: str | None = None
    status: int | None = None
    instances_info: InstancesInfo | None = None
    request: Request | None = None
    available: Available | None = None
    logged_data: LoggedData | None = None
    user_logs: Logs | None = None
    channel_logs: Logs | None = None
    opted_out: OptedOut | None = None
    last_updated: LastUpdated | None = None
    elapsed: Elapsed | None = None

    @staticmethod
    def from_dict(obj: Any) -> "APIZonian":
        assert isinstance(obj, dict)
        error = from_union([from_none, from_str], obj.get("error"))
        status = from_union([from_int, from_none], obj.get("status"))
        instances_info = from_union([InstancesInfo.from_dict, from_none], obj.get("instancesInfo"))
        request = from_union([Request.from_dict, from_none], obj.get("request"))
        available = from_union([Available.from_dict, from_none], obj.get("available"))
        logged_data = from_union([LoggedData.from_dict, from_none], obj.get("loggedData"))
        user_logs = from_union([Logs.from_dict, from_none], obj.get("userLogs"))
        channel_logs = from_union([Logs.from_dict, from_none], obj.get("channelLogs"))
        opted_out = from_union([OptedOut.from_dict, from_none], obj.get("optedOut"))
        last_updated = from_union([LastUpdated.from_dict, from_none], obj.get("lastUpdated"))
        elapsed = from_union([Elapsed.from_dict, from_none], obj.get("elapsed"))
        return APIZonian(
            error,
            status,
            instances_info,
            request,
            available,
            logged_data,
            user_logs,
            channel_logs,
            opted_out,
            last_updated,
            elapsed,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.error is not None:
            result["error"] = from_union([from_none, from_str], self.error)
        if self.status is not None:
            result["status"] = from_union([from_int, from_none], self.status)
        if self.instances_info is not None:
            result["instancesInfo"] = from_union([lambda x: to_class(InstancesInfo, x), from_none], self.instances_info)
        if self.request is not None:
            result["request"] = from_union([lambda x: to_class(Request, x), from_none], self.request)
        if self.available is not None:
            result["available"] = from_union([lambda x: to_class(Available, x), from_none], self.available)
        if self.logged_data is not None:
            result["loggedData"] = from_union([lambda x: to_class(LoggedData, x), from_none], self.logged_data)
        if self.user_logs is not None:
            result["userLogs"] = from_union([lambda x: to_class(Logs, x), from_none], self.user_logs)
        if self.channel_logs is not None:
            result["channelLogs"] = from_union([lambda x: to_class(Logs, x), from_none], self.channel_logs)
        if self.opted_out is not None:
            result["optedOut"] = from_union([lambda x: to_class(OptedOut, x), from_none], self.opted_out)
        if self.last_updated is not None:
            result["lastUpdated"] = from_union([lambda x: to_class(LastUpdated, x), from_none], self.last_updated)
        if self.elapsed is not None:
            result["elapsed"] = from_union([lambda x: to_class(Elapsed, x), from_none], self.elapsed)
        return result


def api_zonian_from_dict(s: Any) -> APIZonian:
    return APIZonian.from_dict(s)


def api_zonian_to_dict(x: APIZonian) -> Any:
    return to_class(APIZonian, x)
