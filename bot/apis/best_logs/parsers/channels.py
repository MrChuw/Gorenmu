# -*- coding: utf-8 -*-
from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Optional, TypeVar

from .shared import (
    from_bool,
    from_datetime,
    from_dict,
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
class Channel:
    name: Optional[str] = None
    user_id: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "Channel":
        assert isinstance(obj, dict)
        name = from_union([from_str, from_none], obj.get("name"))
        user_id = from_union([from_none, lambda x: int(from_str(x))], obj.get("userID"))
        return Channel(name, user_id)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.name is not None:
            result["name"] = from_union([from_str, from_none], self.name)
        if self.user_id is not None:
            result["userID"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x)),
                ],
                self.user_id,
            )
        return result


@dataclass
class Channels:
    channels: Optional[List[Channel]] = None

    @staticmethod
    def from_dict(obj: Any) -> "Channels":
        assert isinstance(obj, dict)
        channels = from_union([lambda x: from_list(Channel.from_dict, x), from_none], obj.get("channels"))
        return Channels(channels)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.channels is not None:
            result["channels"] = from_union(
                [lambda x: from_list(lambda x: to_class(Channel, x), x), from_none], self.channels
            )
        return result


def channels_from_dict(s: Any) -> Channels:
    return Channels.from_dict(s)


def channels_to_dict(x: Channels) -> Any:
    return to_class(Channels, x)
