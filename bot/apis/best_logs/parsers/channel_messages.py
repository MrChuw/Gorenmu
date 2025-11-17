# -*- coding: utf-8 -*-
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, TypeVar
from uuid import UUID

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
class Tags:
    badges: Optional[str] = None
    badge_info: Optional[str] = None
    id: Optional[UUID] = None
    user_id: Optional[int] = None
    color: Optional[str] = None
    flags: Optional[str] = None
    display_name: Optional[str] = None
    vip: Optional[int] = None
    user_type: Optional[str] = None
    emotes: Optional[str] = None
    tmi_sent_ts: Optional[str] = None
    room_id: Optional[int] = None
    subscriber: Optional[int] = None
    mod: Optional[int] = None
    reply_thread_parent_msg_id: Optional[UUID] = None
    reply_parent_msg_body: Optional[str] = None
    reply_parent_user_login: Optional[str] = None
    reply_parent_msg_id: Optional[UUID] = None
    reply_parent_display_name: Optional[str] = None
    reply_parent_user_id: Optional[int] = None
    reply_thread_parent_user_id: Optional[int] = None
    reply_thread_parent_display_name: Optional[str] = None
    reply_thread_parent_user_login: Optional[str] = None
    emote_only: Optional[int] = None
    target_user_id: Optional[int] = None
    ban_duration: Optional[int] = None
    client_nonce: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "Tags":
        assert isinstance(obj, dict)
        badges = from_union([from_str, from_none], obj.get("badges"))
        badge_info = from_union([from_str, from_none], obj.get("badge-info"))
        id = from_union([lambda x: UUID(x), from_none], obj.get("id"))
        user_id = from_union([from_none, lambda x: int(from_str(x))], obj.get("user-id"))
        color = from_union([from_str, from_none], obj.get("color"))
        flags = from_union([from_str, from_none], obj.get("flags"))
        display_name = from_union([from_str, from_none], obj.get("display-name"))
        vip = from_union([from_none, lambda x: int(from_str(x))], obj.get("vip"))
        user_type = from_union([from_str, from_none], obj.get("user-type"))
        emotes = from_union([from_str, from_none], obj.get("emotes"))
        tmi_sent_ts = from_union([from_str, from_none], obj.get("tmi-sent-ts"))
        room_id = from_union([from_none, lambda x: int(from_str(x))], obj.get("room-id"))
        subscriber = from_union([from_none, lambda x: int(from_str(x))], obj.get("subscriber"))
        mod = from_union([from_none, lambda x: int(from_str(x))], obj.get("mod"))
        reply_thread_parent_msg_id = from_union([lambda x: UUID(x), from_none], obj.get("reply-thread-parent-msg-id"))
        reply_parent_msg_body = from_union([from_str, from_none], obj.get("reply-parent-msg-body"))
        reply_parent_user_login = from_union([from_str, from_none], obj.get("reply-parent-user-login"))
        reply_parent_msg_id = from_union([lambda x: UUID(x), from_none], obj.get("reply-parent-msg-id"))
        reply_parent_display_name = from_union([from_str, from_none], obj.get("reply-parent-display-name"))
        reply_parent_user_id = from_union([from_none, lambda x: int(from_str(x))], obj.get("reply-parent-user-id"))
        reply_thread_parent_user_id = from_union(
            [from_none, lambda x: int(from_str(x))], obj.get("reply-thread-parent-user-id")
        )
        reply_thread_parent_display_name = from_union(
            [from_str, from_none], obj.get("reply-thread-parent-display-name")
        )
        reply_thread_parent_user_login = from_union([from_str, from_none], obj.get("reply-thread-parent-user-login"))
        emote_only = from_union([from_none, lambda x: int(from_str(x))], obj.get("emote-only"))
        target_user_id = from_union([from_none, lambda x: int(from_str(x))], obj.get("target-user-id"))
        ban_duration = from_union([from_none, lambda x: int(from_str(x))], obj.get("ban-duration"))
        client_nonce = from_union([from_str, from_none], obj.get("client-nonce"))
        return Tags(
            badges,
            badge_info,
            id,
            user_id,
            color,
            flags,
            display_name,
            vip,
            user_type,
            emotes,
            tmi_sent_ts,
            room_id,
            subscriber,
            mod,
            reply_thread_parent_msg_id,
            reply_parent_msg_body,
            reply_parent_user_login,
            reply_parent_msg_id,
            reply_parent_display_name,
            reply_parent_user_id,
            reply_thread_parent_user_id,
            reply_thread_parent_display_name,
            reply_thread_parent_user_login,
            emote_only,
            target_user_id,
            ban_duration,
            client_nonce,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.badges is not None:
            result["badges"] = from_union([from_str, from_none], self.badges)
        if self.badge_info is not None:
            result["badge-info"] = from_union([from_str, from_none], self.badge_info)
        if self.id is not None:
            result["id"] = from_union([lambda x: str(x), from_none], self.id)
        if self.user_id is not None:
            result["user-id"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x)),
                ],
                self.user_id,
            )
        if self.color is not None:
            result["color"] = from_union([from_str, from_none], self.color)
        if self.flags is not None:
            result["flags"] = from_union([from_str, from_none], self.flags)
        if self.display_name is not None:
            result["display-name"] = from_union([from_str, from_none], self.display_name)
        if self.vip is not None:
            result["vip"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x)),
                ],
                self.vip,
            )
        if self.user_type is not None:
            result["user-type"] = from_union([from_str, from_none], self.user_type)
        if self.emotes is not None:
            result["emotes"] = from_union([from_str, from_none], self.emotes)
        if self.tmi_sent_ts is not None:
            result["tmi-sent-ts"] = from_union([from_str, from_none], self.tmi_sent_ts)
        if self.room_id is not None:
            result["room-id"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x)),
                ],
                self.room_id,
            )
        if self.subscriber is not None:
            result["subscriber"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x)),
                ],
                self.subscriber,
            )
        if self.mod is not None:
            result["mod"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x)),
                ],
                self.mod,
            )
        if self.reply_thread_parent_msg_id is not None:
            result["reply-thread-parent-msg-id"] = from_union(
                [lambda x: str(x), from_none], self.reply_thread_parent_msg_id
            )
        if self.reply_parent_msg_body is not None:
            result["reply-parent-msg-body"] = from_union([from_str, from_none], self.reply_parent_msg_body)
        if self.reply_parent_user_login is not None:
            result["reply-parent-user-login"] = from_union([from_str, from_none], self.reply_parent_user_login)
        if self.reply_parent_msg_id is not None:
            result["reply-parent-msg-id"] = from_union([lambda x: str(x), from_none], self.reply_parent_msg_id)
        if self.reply_parent_display_name is not None:
            result["reply-parent-display-name"] = from_union([from_str, from_none], self.reply_parent_display_name)
        if self.reply_parent_user_id is not None:
            result["reply-parent-user-id"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x)),
                ],
                self.reply_parent_user_id,
            )
        if self.reply_thread_parent_user_id is not None:
            result["reply-thread-parent-user-id"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x)),
                ],
                self.reply_thread_parent_user_id,
            )
        if self.reply_thread_parent_display_name is not None:
            result["reply-thread-parent-display-name"] = from_union(
                [from_str, from_none], self.reply_thread_parent_display_name
            )
        if self.reply_thread_parent_user_login is not None:
            result["reply-thread-parent-user-login"] = from_union(
                [from_str, from_none], self.reply_thread_parent_user_login
            )
        if self.emote_only is not None:
            result["emote-only"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x)),
                ],
                self.emote_only,
            )
        if self.target_user_id is not None:
            result["target-user-id"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x)),
                ],
                self.target_user_id,
            )
        if self.ban_duration is not None:
            result["ban-duration"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x)),
                ],
                self.ban_duration,
            )
        if self.client_nonce is not None:
            result["client-nonce"] = from_union([from_str, from_none], self.client_nonce)
        return result


@dataclass
class Message:
    text: Optional[str] = None
    display_name: Optional[str] = None
    channel: Optional[str] = None
    timestamp: Optional[datetime] = None
    id: Optional[str] = None
    tags: Optional[Tags] = None
    username: Optional[str] = None
    raw: Optional[str] = None
    type: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "Message":
        assert isinstance(obj, dict)
        text = from_union([from_str, from_none], obj.get("text"))
        display_name = from_union([from_str, from_none], obj.get("displayName"))
        channel = from_union([from_str, from_none], obj.get("channel"))
        timestamp = from_union([from_datetime, from_none], obj.get("timestamp"))
        id = from_union([from_str, from_none], obj.get("id"))
        tags = from_union([Tags.from_dict, from_none], obj.get("tags"))
        username = from_union([from_str, from_none], obj.get("username"))
        raw = from_union([from_str, from_none], obj.get("raw"))
        type = from_union([from_int, from_none], obj.get("type"))
        return Message(text, display_name, channel, timestamp, id, tags, username, raw, type)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.text is not None:
            result["text"] = from_union([from_str, from_none], self.text)
        if self.display_name is not None:
            result["displayName"] = from_union([from_str, from_none], self.display_name)
        if self.channel is not None:
            result["channel"] = from_union([from_str, from_none], self.channel)
        if self.timestamp is not None:
            result["timestamp"] = from_union([lambda x: x.isoformat(), from_none], self.timestamp)
        if self.id is not None:
            result["id"] = from_union([from_str, from_none], self.id)
        if self.tags is not None:
            result["tags"] = from_union([lambda x: to_class(Tags, x), from_none], self.tags)
        if self.username is not None:
            result["username"] = from_union([from_str, from_none], self.username)
        if self.raw is not None:
            result["raw"] = from_union([from_str, from_none], self.raw)
        if self.type is not None:
            result["type"] = from_union([from_int, from_none], self.type)
        return result


@dataclass
class ChannelMessages:
    messages: Optional[List[Message]] = None

    @staticmethod
    def from_dict(obj: Any) -> "ChannelMessages":
        assert isinstance(obj, dict)
        messages = from_union([lambda x: from_list(Message.from_dict, x), from_none], obj.get("messages"))
        return ChannelMessages(messages)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.messages is not None:
            result["messages"] = from_union(
                [lambda x: from_list(lambda x: to_class(Message, x), x), from_none], self.messages
            )
        return result


def channel_messages_from_dict(s: Any) -> ChannelMessages:
    return ChannelMessages.from_dict(s)


def channel_messages_to_dict(x: ChannelMessages) -> Any:
    return to_class(ChannelMessages, x)
