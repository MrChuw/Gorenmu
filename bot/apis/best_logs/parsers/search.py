from dataclasses import dataclass
from datetime import datetime
from typing import Any, TypeVar

from .shared import (
    from_datetime,
    from_dict,
    from_int,
    from_list,
    from_none,
    from_str,
    from_union,
    to_class,
)

T = TypeVar("T")


@dataclass
class Message:
    text: str | None = None
    display_name: str | None = None
    timestamp: datetime | None = None
    id: str | None = None
    tags: dict[str, str] | None = None
    username: str | None = None
    channel: str | None = None
    raw: str | None = None
    type: int | None = None

    @staticmethod
    def from_dict(obj: Any) -> "Message":
        assert isinstance(obj, dict)
        text = from_union([from_str, from_none], obj.get("text"))
        display_name = from_union([from_str, from_none], obj.get("displayName"))
        timestamp = from_union([from_datetime, from_none], obj.get("timestamp"))
        id = from_union([from_str, from_none], obj.get("id"))
        tags = from_union([lambda x: from_dict(from_str, x), from_none], obj.get("tags"))
        username = from_union([from_str, from_none], obj.get("username"))
        channel = from_union([from_str, from_none], obj.get("channel"))
        raw = from_union([from_str, from_none], obj.get("raw"))
        type = from_union([from_int, from_none], obj.get("type"))
        return Message(text, display_name, timestamp, id, tags, username, channel, raw, type)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.text is not None:
            result["text"] = from_union([from_str, from_none], self.text)
        if self.display_name is not None:
            result["displayName"] = from_union([lambda x: from_str(x), from_none], self.display_name)
        if self.timestamp is not None:
            result["timestamp"] = from_union([lambda x: x.isoformat(), from_none], self.timestamp)
        if self.id is not None:
            result["id"] = from_union([from_str, from_none], self.id)
        if self.tags is not None:
            result["tags"] = from_union([lambda x: from_dict(from_str, x), from_none], self.tags)
        if self.username is not None:
            result["username"] = from_union([lambda x: from_str(x), from_none], self.username)
        if self.channel is not None:
            result["channel"] = from_union([lambda x: from_str(x), from_none], self.channel)
        if self.raw is not None:
            result["raw"] = from_union([from_str, from_none], self.raw)
        if self.type is not None:
            result["type"] = from_union([from_int, from_none], self.type)
        return result


@dataclass
class Search:
    messages: list[Message] | None = None

    @staticmethod
    def from_dict(obj: Any) -> "Search":
        assert isinstance(obj, dict)
        messages = from_union([lambda x: from_list(Message.from_dict, x), from_none], obj.get("messages"))
        return Search(messages)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.messages is not None:
            result["messages"] = from_union(
                [lambda x: from_list(lambda x: to_class(Message, x), x), from_none],
                self.messages,
            )
        return result
