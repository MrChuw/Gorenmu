# -*- coding: utf-8 -*-
from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Optional, TypeVar

from .shared import (
    from_bool,
    from_datetime,
    from_dict,
    from_int,
    from_list,
    from_none,
    from_str,
    from_union,
    is_type,
    to_class,
)

T = TypeVar("T")


@dataclass
class TopChatter:
    user_id: Optional[int] = None
    user_login: Optional[str] = None
    message_count: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "TopChatter":
        assert isinstance(obj, dict)
        user_id = from_union([from_none, lambda x: int(from_str(x))], obj.get("userId"))
        user_login = from_union([from_str, from_none], obj.get("userLogin"))
        message_count = from_union([from_int, from_none], obj.get("messageCount"))
        return TopChatter(user_id, user_login, message_count)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.user_id is not None:
            result["userId"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x)),
                ],
                self.user_id,
            )
        if self.user_login is not None:
            result["userLogin"] = from_union([from_str, from_none], self.user_login)
        if self.message_count is not None:
            result["messageCount"] = from_union([from_int, from_none], self.message_count)
        return result


@dataclass
class ChannelStats:
    message_count: Optional[int] = None
    top_chatters: Optional[List[TopChatter]] = None

    @staticmethod
    def from_dict(obj: Any) -> "ChannelStats":
        assert isinstance(obj, dict)
        message_count = from_union([from_int, from_none], obj.get("messageCount"))
        top_chatters = from_union([lambda x: from_list(TopChatter.from_dict, x), from_none], obj.get("topChatters"))
        return ChannelStats(message_count, top_chatters)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.message_count is not None:
            result["messageCount"] = from_union([from_int, from_none], self.message_count)
        if self.top_chatters is not None:
            result["topChatters"] = from_union(
                [lambda x: from_list(lambda x: to_class(TopChatter, x), x), from_none], self.top_chatters
            )
        return result
