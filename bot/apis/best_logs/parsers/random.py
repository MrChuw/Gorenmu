# -*- coding: utf-8 -*-
from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Optional, TypeVar
from uuid import UUID

from .shared import from_datetime, from_int, from_list, from_none, from_str, from_union, is_type, to_class

T = TypeVar("T")


@dataclass
class Tags:
    id: Optional[UUID] = None
    room_id: Optional[int] = None
    badges: Optional[str] = None
    flags: Optional[str] = None
    tmi_sent_ts: Optional[str] = None
    badge_info: Optional[str] = None
    color: Optional[str] = None
    emotes: Optional[str] = None
    user_type: Optional[str] = None
    user_id: Optional[int] = None
    display_name: Optional[str] = None
    mod: Optional[int] = None
    subscriber: Optional[int] = None
    vip: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "Tags":
        assert isinstance(obj, dict)
        id = from_union([lambda x: UUID(x), from_none], obj.get("id"))
        room_id = from_union([from_none, lambda x: int(from_str(x))], obj.get("room-id"))
        badges = from_union([from_str, from_none], obj.get("badges"))
        flags = from_union([from_str, from_none], obj.get("flags"))
        tmi_sent_ts = from_union([from_str, from_none], obj.get("tmi-sent-ts"))
        badge_info = from_union([from_str, from_none], obj.get("badge-info"))
        color = from_union([from_str, from_none], obj.get("color"))
        emotes = from_union([from_str, from_none], obj.get("emotes"))
        user_type = from_union([from_str, from_none], obj.get("user-type"))
        user_id = from_union([from_none, lambda x: int(from_str(x))], obj.get("user-id"))
        display_name = from_union([from_str, from_none], obj.get("display-name"))
        mod = from_union([from_none, lambda x: int(from_str(x))], obj.get("mod"))
        subscriber = from_union([from_none, lambda x: int(from_str(x))], obj.get("subscriber"))
        vip = from_union([from_none, lambda x: int(from_str(x))], obj.get("vip"))
        return Tags(
            id,
            room_id,
            badges,
            flags,
            tmi_sent_ts,
            badge_info,
            color,
            emotes,
            user_type,
            user_id,
            display_name,
            mod,
            subscriber,
            vip,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = from_union([lambda x: str(x), from_none], self.id)
        if self.room_id is not None:
            result["room-id"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x)),
                ],
                self.room_id,
            )
        if self.badges is not None:
            result["badges"] = from_union([from_str, from_none], self.badges)
        if self.flags is not None:
            result["flags"] = from_union([from_str, from_none], self.flags)
        if self.tmi_sent_ts is not None:
            result["tmi-sent-ts"] = from_union([from_str, from_none], self.tmi_sent_ts)
        if self.badge_info is not None:
            result["badge-info"] = from_union([from_str, from_none], self.badge_info)
        if self.color is not None:
            result["color"] = from_union([from_str, from_none], self.color)
        if self.emotes is not None:
            result["emotes"] = from_union([from_str, from_none], self.emotes)
        if self.user_type is not None:
            result["user-type"] = from_union([from_str, from_none], self.user_type)
        if self.user_id is not None:
            result["user-id"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x)),
                ],
                self.user_id,
            )
        if self.display_name is not None:
            result["display-name"] = from_union([from_str, from_none], self.display_name)
        if self.mod is not None:
            result["mod"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x)),
                ],
                self.mod,
            )
        if self.subscriber is not None:
            result["subscriber"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x)),
                ],
                self.subscriber,
            )
        if self.vip is not None:
            result["vip"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x)),
                ],
                self.vip,
            )
        return result


@dataclass
class Message:
    text: Optional[str] = None
    display_name: Optional[str] = None
    timestamp: Optional[datetime] = None
    id: Optional[UUID] = None
    tags: Optional[Tags] = None
    username: Optional[str] = None
    channel: Optional[str] = None
    raw: Optional[str] = None
    type: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "Message":
        assert isinstance(obj, dict)
        text = from_union([from_str, from_none], obj.get("text"))
        display_name = from_union([from_str, from_none], obj.get("displayName"))
        timestamp = from_union([from_datetime, from_none], obj.get("timestamp"))
        id = from_union([lambda x: UUID(x), from_none], obj.get("id"))
        tags = from_union([Tags.from_dict, from_none], obj.get("tags"))
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
            result["displayName"] = from_union([from_str, from_none], self.display_name)
        if self.timestamp is not None:
            result["timestamp"] = from_union([lambda x: x.isoformat(), from_none], self.timestamp)
        if self.id is not None:
            result["id"] = from_union([lambda x: str(x), from_none], self.id)
        if self.tags is not None:
            result["tags"] = from_union([lambda x: to_class(Tags, x), from_none], self.tags)
        if self.username is not None:
            result["username"] = from_union([from_str, from_none], self.username)
        if self.channel is not None:
            result["channel"] = from_union([from_str, from_none], self.channel)
        if self.raw is not None:
            result["raw"] = from_union([from_str, from_none], self.raw)
        if self.type is not None:
            result["type"] = from_union([from_int, from_none], self.type)
        return result


@dataclass
class Random:
    messages: Optional[List[Message]] = None

    @staticmethod
    def from_dict(obj: Any) -> "Random":
        assert isinstance(obj, dict)
        messages = from_union([lambda x: from_list(Message.from_dict, x), from_none], obj.get("messages"))
        return Random(messages)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.messages is not None:
            result["messages"] = from_union(
                [lambda x: from_list(lambda x: to_class(Message, x), x), from_none], self.messages
            )
        return result


def random_from_dict(s: Any) -> Random:
    return Random.from_dict(s)


def random_to_dict(x: Random) -> Any:
    return to_class(Random, x)
