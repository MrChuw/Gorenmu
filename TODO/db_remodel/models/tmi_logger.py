import datetime
from datetime import datetime

import humanize
from tortoise import fields
from tortoise.models import Model

# Local
from .timezonefield import DatetimeTzField


humanize.activate("pt_BR")
"""Fields

: fields.CharField = fields.TextField()
: fields.BooleanField = fields.BooleanField(default=None, null=True)
: fields.CharField = fields.CharField(max_length=255, default=None, null=True)
: fields.JSONField = fields.JSONField(default=None, null=True)
: fields.IntField = fields.IntField(default=None, null=True)

"""


class Base(Model):
    id = fields.IntField(pk=True)

    class Meta:
        abstract = True

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"


class Twitch_Tmi(Base):
    created_at: DatetimeTzField = DatetimeTzField(auto_now_add=True)
    raw_data: fields.BinaryField = fields.BinaryField()
    commando: fields.CharField = fields.CharField(max_length=50)
    channel_id: fields.IntField = fields.IntField(default=None, null=True)
    user_id: fields.IntField = fields.IntField(default=None, null=True)

    class Meta:
        table = "tmi_logger_master"


class Channel_Tmi(Base):
    twitch_tmi: fields.ForeignKeyRelation["Twitch_Tmi"] = fields.ForeignKeyField(
        "models.Twitch_Tmi", related_name="Channel"
    )
    name: fields.CharField = fields.CharField(max_length=255, default=None, null=True)
    is_emote_only: fields.BooleanField = fields.BooleanField(default=None, null=True)
    is_subs_only: fields.BooleanField = fields.BooleanField(default=None, null=True)
    is_followers_only: fields.BooleanField = fields.BooleanField(default=None, null=True)
    is_unique_only: fields.BooleanField = fields.BooleanField(default=None, null=True)
    follower_only_delay: fields.IntField = fields.IntField(default=None, null=True)
    room_id: fields.IntField = fields.IntField(default=None, null=True)
    slow: fields.IntField = fields.IntField(default=None, null=True)

    class Meta:
        table = "tmi_logger_channel"


class User_Tmi(Base):
    tmi_logger: fields.ForeignKeyRelation["Twitch_Tmi"] = fields.ForeignKeyField(
        "models.Twitch_Tmi", related_name="User"
    )
    name: fields.CharField = fields.CharField(max_length=255, default=None, null=True)
    badge_info: fields.JSONField = fields.JSONField(default=None, null=True)
    badges: fields.JSONField = fields.JSONField(default=None, null=True)
    color: fields.CharField = fields.CharField(max_length=255, default=None, null=True)
    display_name: fields.CharField = fields.CharField(max_length=255, default=None, null=True)
    mod: fields.BooleanField = fields.BooleanField(default=None, null=True)
    subscriber: fields.BooleanField = fields.BooleanField(default=None, null=True)
    turbo: fields.BooleanField = fields.BooleanField(default=None, null=True)
    user_id: fields.IntField = fields.IntField(default=None, null=True)
    user_type: fields.CharField = fields.CharField(max_length=255, default=None, null=True)
    vip: fields.BooleanField = fields.BooleanField(default=None, null=True)
    content: fields.CharField = fields.CharField(max_length=1000, default=None, null=True)
    channel_id: fields.IntField = fields.IntField(default=None, null=True)

    class Meta:
        table = "tmi_logger_user"


class MessageDeleted_Tmi(Base):
    tmi_logger: fields.ForeignKeyRelation["Twitch_Tmi"] = fields.ForeignKeyField(
        "models.Twitch_Tmi", related_name="MessageDeleted"
    )
    room_name: fields.CharField = fields.CharField(max_length=255, default=None, null=True)
    message: fields.CharField = fields.CharField(max_length=255, default=None, null=True)
    user_name: fields.CharField = fields.CharField(max_length=255, default=None, null=True)
    message_id: fields.CharField = fields.CharField(max_length=255, default=None, null=True)
    sent_times_stamp: DatetimeTzField = DatetimeTzField(default=None, null=True)

    class Meta:
        table = "tmi_logger_message_deleted"


class JoinChannelEvent_Tmi(Base):
    tmi_logger: fields.ForeignKeyRelation["Twitch_Tmi"] = fields.ForeignKeyField(
        "models.Twitch_Tmi", related_name="JoinChannel"
    )
    channel: fields.CharField = fields.CharField(max_length=255, default=None, null=True)
    user: fields.CharField = fields.CharField(max_length=255, default=None, null=True)

    class Meta:
        table = "tmi_logger_join_channel"


class PartChannelEvent_Tmi(Base):
    tmi_logger: fields.ForeignKeyRelation["Twitch_Tmi"] = fields.ForeignKeyField(
        "models.Twitch_Tmi", related_name="PartChannel"
    )
    channel: fields.CharField = fields.CharField(max_length=255, default=None, null=True)
    user: fields.CharField = fields.CharField(max_length=255, default=None, null=True)

    class Meta:
        table = "tmi_logger_part_channel"


class ChatMessageEvent_Tmi(Base):
    tmi_logger: fields.ForeignKeyRelation["Twitch_Tmi"] = fields.ForeignKeyField(
        "models.Twitch_Tmi", related_name="ChannelMessage"
    )
    parsed: fields.JSONField = fields.JSONField(default=None, null=True)
    content: fields.CharField = fields.CharField(max_length=1000, default=None, null=True)
    bits: fields.IntField = fields.IntField(default=None, null=True)
    sent_timestamp: DatetimeTzField = DatetimeTzField(default=None, null=True)
    reply_parent_msg_id: fields.CharField = fields.CharField(
        max_length=255, default=None, null=True
    )
    reply_parent_user_id: fields.CharField = fields.CharField(
        max_length=255, default=None, null=True
    )
    reply_parent_user_login: fields.CharField = fields.CharField(
        max_length=255, default=None, null=True
    )
    reply_parent_display_name: fields.CharField = fields.CharField(
        max_length=255, default=None, null=True
    )
    reply_parent_msg_body: fields.CharField = fields.CharField(
        max_length=255, default=None, null=True
    )
    emotes: fields.JSONField = fields.JSONField(default=None, null=True)
    msg_id: fields.CharField = fields.CharField(max_length=255, default=None, null=True)

    badge_info: fields.JSONField = fields.JSONField(default=None, null=True)
    badge: fields.JSONField = fields.JSONField(default=None, null=True)
    color: fields.CharField = fields.CharField(max_length=255, default=None, null=True)
    first_msg: fields.IntField = fields.IntField(default=None, null=True)
    mod: fields.IntField = fields.IntField(default=None, null=True)
    returning_chatter: fields.IntField = fields.IntField(default=None, null=True)
    subscriber: fields.IntField = fields.IntField(default=None, null=True)
    turbo: fields.IntField = fields.IntField(default=None, null=True)
    user_type: fields.CharField = fields.CharField(max_length=255, default=None, null=True)
    user_nick: fields.CharField = fields.CharField(max_length=255, default=None, null=True)
    user_id: fields.IntField = fields.IntField(default=None, null=True)
    channel_id: fields.IntField = fields.IntField(default=None, null=True)

    class Meta:
        table = "tmi_logger_chat_message"


class ChannelSubEvent_Tmi(Base):
    tmi_logger: fields.ForeignKeyRelation["Twitch_Tmi"] = fields.ForeignKeyField(
        "models.Twitch_Tmi", related_name="ChannelSub"
    )
    sub_parsed: fields.JSONField = fields.JSONField(default=None, null=True)
    sub_type: fields.CharField = fields.CharField(max_length=255, default=None, null=True)
    sub_message: fields.CharField = fields.CharField(max_length=255, default=None, null=True)
    sub_plan: fields.CharField = fields.CharField(max_length=255, default=None, null=True)
    sub_plan_name: fields.CharField = fields.CharField(max_length=255, default=None, null=True)
    system_message: fields.CharField = fields.CharField(max_length=255, default=None, null=True)

    badge_info: fields.JSONField = fields.JSONField(default=None, null=True)
    badge: fields.JSONField = fields.JSONField(default=None, null=True)
    color: fields.CharField = fields.CharField(max_length=255, default=None, null=True)
    display_name: fields.CharField = fields.CharField(max_length=255, default=None, null=True)
    emotes: fields.CharField = fields.CharField(max_length=255, default=None, null=True)
    sub_id: fields.CharField = fields.CharField(max_length=255, default=None, null=True)
    login: fields.CharField = fields.CharField(max_length=255, default=None, null=True)
    mod: fields.IntField = fields.IntField(default=None, null=True)
    msg_param_cumulative_months: fields.IntField = fields.IntField(default=None, null=True)
    msg_param_months: fields.IntField = fields.IntField(default=None, null=True)
    msg_param_multimonth_duration: fields.IntField = fields.IntField(default=None, null=True)
    msg_param_multimonth_tenure: fields.IntField = fields.IntField(default=None, null=True)
    msg_param_should_share_streak: fields.IntField = fields.IntField(default=None, null=True)
    msg_param_was_gifted: fields.BooleanField = fields.BooleanField(default=None, null=True)
    subscriber: fields.CharField = fields.CharField(max_length=255, default=None, null=True)
    tmi_sent_ts: fields.IntField = fields.IntField(default=None, null=True)
    user_type: fields.CharField = fields.CharField(max_length=255, default=None, null=True)

    class Meta:
        table = "tmi_logger_channel_sub"


class ClearChatEvent_Tmi(Base):
    tmi_logger: fields.ForeignKeyRelation["Twitch_Tmi"] = fields.ForeignKeyField(
        "models.Twitch_Tmi", related_name="ClearChat"
    )
    room_name: fields.CharField = fields.CharField(max_length=255, default=None, null=True)
    user_name: fields.CharField = fields.CharField(max_length=255, default=None, null=True)
    room_id: fields.IntField = fields.IntField(default=None, null=True)
    duration: fields.IntField = fields.IntField(default=None, null=True)
    banned_user_id: fields.IntField = fields.IntField(default=None, null=True)
    sent_timestamp: DatetimeTzField = DatetimeTzField(default=None, null=True)

    class Meta:
        table = "tmi_logger_clear_chat"


class WhisperEvent_Tmi(Base):
    tmi_logger: fields.ForeignKeyRelation["Twitch_Tmi"] = fields.ForeignKeyField(
        "models.Twitch_Tmi", related_name="Whisper"
    )
    whisper_parsed: fields.JSONField = fields.JSONField(default=None, null=True)
    whisper_message: fields.CharField = fields.CharField(max_length=800, default=None, null=True)

    class Meta:
        table = "tmi_logger_whisper"


class NoticeEvent_Tmi(Base):
    tmi_logger: fields.ForeignKeyRelation["Twitch_Tmi"] = fields.ForeignKeyField(
        "models.Twitch_Tmi", related_name="Notice"
    )
    room_name: fields.CharField = fields.CharField(max_length=255, default=None, null=True)
    msg_id: fields.CharField = fields.CharField(max_length=255, default=None, null=True)
    message: fields.CharField = fields.CharField(max_length=255, default=None, null=True)

    class Meta:
        table = "tmi_logger_notice"
