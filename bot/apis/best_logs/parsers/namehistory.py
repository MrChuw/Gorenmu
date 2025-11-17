# -*- coding: utf-8 -*-
from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Optional, TypeVar

T = TypeVar("T")

from .shared import from_datetime, from_list, from_none, from_str, from_union, to_class


@dataclass
class NameHistory:
    user_login: Optional[str] = None
    last_timestamp: Optional[datetime] = None
    first_timestamp: Optional[datetime] = None

    @staticmethod
    def from_dict(obj: Any) -> "NameHistory":
        assert isinstance(obj, dict)
        user_login = from_union([from_str, from_none], obj.get("user_login"))
        last_timestamp = from_union([from_datetime, from_none], obj.get("last_timestamp"))
        first_timestamp = from_union([from_datetime, from_none], obj.get("first_timestamp"))
        return NameHistory(user_login, last_timestamp, first_timestamp)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.user_login is not None:
            result["user_login"] = from_union([from_str, from_none], self.user_login)
        if self.last_timestamp is not None:
            result["last_timestamp"] = from_union([lambda x: x.isoformat(), from_none], self.last_timestamp)
        if self.first_timestamp is not None:
            result["first_timestamp"] = from_union([lambda x: x.isoformat(), from_none], self.first_timestamp)
        return result

    @staticmethod
    def from_dict_alt(s: Any) -> List["NameHistory"]:
        return from_list(NameHistory.from_dict, s)

    @staticmethod
    def name_history_to_dict(x: List["NameHistory"]) -> Any:
        return from_list(lambda x: to_class(NameHistory, x), x)
