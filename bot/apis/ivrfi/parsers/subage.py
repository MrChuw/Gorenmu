from dataclasses import dataclass
from datetime import datetime
from typing import Any, TypeVar

from bot.apis.ivrfi.parsers.common import (
    from_bool,
    from_datetime,
    from_int,
    from_none,
    from_str,
    from_union,
    is_type,
    to_class,
)

T = TypeVar("T")


@dataclass
class Channel:
    id: int | None = None
    login: str | None = None
    display_name: str | None = None

    @staticmethod
    def from_dict(obj: Any) -> "Channel":
        assert isinstance(obj, dict)
        id = from_union([from_none, lambda x: int(from_str(x))], obj.get("id"))
        login = from_union([from_str, from_none], obj.get("login"))
        display_name = from_union([from_str, from_none], obj.get("displayName"))
        return Channel(id, login, display_name)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x)),
                ],
                self.id,
            )
        if self.login is not None:
            result["login"] = from_union([from_str, from_none], self.login)
        if self.display_name is not None:
            result["displayName"] = from_union([from_str, from_none], self.display_name)
        return result


@dataclass
class Cumulative:
    elapsed_days: int | None = None
    days_remaining: int | None = None
    months: int | None = None
    end: datetime | None = None
    start: datetime | None = None

    @staticmethod
    def from_dict(obj: Any) -> "Cumulative":
        assert isinstance(obj, dict)
        elapsed_days = from_union([from_int, from_none], obj.get("elapsedDays"))
        days_remaining = from_union([from_int, from_none], obj.get("daysRemaining"))
        months = from_union([from_int, from_none], obj.get("months"))
        end = from_union([from_datetime, from_none], obj.get("end"))
        start = from_union([from_datetime, from_none], obj.get("start"))
        return Cumulative(elapsed_days, days_remaining, months, end, start)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.elapsed_days is not None:
            result["elapsedDays"] = from_union([from_int, from_none], self.elapsed_days)
        if self.days_remaining is not None:
            result["daysRemaining"] = from_union([from_int, from_none], self.days_remaining)
        if self.months is not None:
            result["months"] = from_union([from_int, from_none], self.months)
        if self.end is not None:
            result["end"] = from_union([lambda x: x.isoformat(), from_none], self.end)
        if self.start is not None:
            result["start"] = from_union([lambda x: x.isoformat(), from_none], self.start)
        return result


@dataclass
class GiftMeta:
    gift_date: datetime | None = None
    gifter: Channel | None = None

    @staticmethod
    def from_dict(obj: Any) -> "GiftMeta":
        assert isinstance(obj, dict)
        gift_date = from_union([from_datetime, from_none], obj.get("giftDate"))
        gifter = from_union([Channel.from_dict, from_none], obj.get("gifter"))
        return GiftMeta(gift_date, gifter)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.gift_date is not None:
            result["giftDate"] = from_union([lambda x: x.isoformat(), from_none], self.gift_date)
        if self.gifter is not None:
            result["gifter"] = from_union([lambda x: to_class(Channel, x), from_none], self.gifter)
        return result


@dataclass
class Meta:
    type: str | None = None
    tier: int | None = None
    ends_at: datetime | None = None
    renews_at: datetime | None = None
    gift_meta: GiftMeta | None = None

    @staticmethod
    def from_dict(obj: Any) -> "Meta":
        assert isinstance(obj, dict)
        type = from_union([from_str, from_none], obj.get("type"))
        tier = from_union([from_none, lambda x: int(from_str(x))], obj.get("tier"))
        ends_at = from_union([from_datetime, from_none], obj.get("endsAt"))
        renews_at = from_union([from_datetime, from_none], obj.get("renewsAt"))
        gift_meta = from_union([GiftMeta.from_dict, from_none], obj.get("giftMeta"))
        return Meta(type, tier, ends_at, renews_at, gift_meta)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.type is not None:
            result["type"] = from_union([from_str, from_none], self.type)
        if self.tier is not None:
            result["tier"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x)),
                ],
                self.tier,
            )
        if self.ends_at is not None:
            result["endsAt"] = from_union([lambda x: x.isoformat(), from_none], self.ends_at)
        if self.renews_at is not None:
            result["renewsAt"] = from_union([lambda x: x.isoformat(), from_none], self.renews_at)
        if self.gift_meta is not None:
            result["giftMeta"] = from_union([lambda x: to_class(GiftMeta, x), from_none], self.gift_meta)
        return result


@dataclass
class SubAge:
    user: Channel | None = None
    channel: Channel | None = None
    status_hidden: bool | None = None
    followed_at: datetime | None = None
    streak: Cumulative | None = None
    cumulative: Cumulative | None = None
    meta: Meta | None = None

    @staticmethod
    def from_dict(obj: Any) -> "SubAge":
        assert isinstance(obj, dict)
        user = from_union([Channel.from_dict, from_none], obj.get("user"))
        channel = from_union([Channel.from_dict, from_none], obj.get("channel"))
        status_hidden = from_union([from_bool, from_none], obj.get("statusHidden"))
        followed_at = from_union([from_datetime, from_none], obj.get("followedAt"))
        streak = from_union([from_none, Cumulative.from_dict], obj.get("streak"))
        cumulative = from_union([from_none, Cumulative.from_dict], obj.get("cumulative"))
        meta = from_union([from_none, Meta.from_dict], obj.get("meta"))
        return SubAge(user, channel, status_hidden, followed_at, streak, cumulative, meta)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.user is not None:
            result["user"] = from_union([lambda x: to_class(Channel, x), from_none], self.user)
        if self.channel is not None:
            result["channel"] = from_union([lambda x: to_class(Channel, x), from_none], self.channel)
        if self.status_hidden is not None:
            result["statusHidden"] = from_union([from_bool, from_none], self.status_hidden)
        if self.followed_at is not None:
            result["followedAt"] = from_union([lambda x: x.isoformat(), from_none], self.followed_at)
        if self.streak is not None:
            result["streak"] = from_union([from_none, lambda x: to_class(Cumulative, x)], self.streak)
        if self.cumulative is not None:
            result["cumulative"] = from_union([from_none, lambda x: to_class(Cumulative, x)], self.cumulative)
        if self.meta is not None:
            result["meta"] = from_union([from_none, lambda x: to_class(Meta, x)], self.meta)
        return result


def sub_age_from_dict(s: Any) -> SubAge:
    return SubAge.from_dict(s)


def sub_age_to_dict(x: SubAge) -> Any:
    return to_class(SubAge, x)
