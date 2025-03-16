from __future__ import annotations

from typing import Coroutine, List, Optional, TYPE_CHECKING, Union

from tortoise import fields
from urlextract import URLExtract

from bot.models.base import (
    Base, BoolFieldBool, CharFieldStr, ContentMixin, DatetimeTzField, TimestampMixin, UserMixin,
)
from bot.models.User_extras import (
    Annotation, Bug, Cookies, Copypasta, Imgur, ImgurAggregate, MessagesLog, NickHistory, Pets, Player, PlayerTower,
    Reminder, Status, Suggest,
)

from zoneinfo import ZoneInfo
from datetime import datetime

if TYPE_CHECKING:
    from bot.ext.commands import Context
    from bot.translations import Translations


class User(Base, UserMixin, TimestampMixin, ContentMixin):
    channel: CharFieldStr = fields.CharField(max_length=64, null=True, description="Twitch channel")
    saved_color: CharFieldStr = fields.CharField(max_length=7, null=True, description="Twitch color")
    city: CharFieldStr = fields.CharField(max_length=100, null=True)
    ping: BoolFieldBool = fields.BooleanField(default=True)
    mention: BoolFieldBool = fields.BooleanField(default=True)
    block: BoolFieldBool = fields.BooleanField(default=False)
    sponsor: BoolFieldBool = fields.BooleanField(default=True)
    nickname: CharFieldStr = fields.CharField(max_length=32, null=True)
    timestamp: DatetimeTzField = fields.DatetimeField(null=True)
    language: CharFieldStr = fields.CharField(max_length=32, null=True)
    timezone: CharFieldStr = fields.CharField(max_length=50, default="UTC")
    cookies: List[Cookies] = fields.ReverseRelation["Cookies"]
    player: List[Player] = fields.ReverseRelation["Player"]
    pets: List[Pets] = fields.ReverseRelation["Pets"]
    player_torre: List[PlayerTower] = fields.ReverseRelation["Player_torre"]
    suggest: List[Suggest] = fields.ReverseRelation["Suggest"]
    bug: List[Bug] = fields.ReverseRelation["Bug"]
    annotation: List[Annotation] = fields.ReverseRelation["Annotation"]
    nick_history: List[Union[NickHistory, str]] = fields.ReverseRelation["NickHistory"]
    status: List[Status] = fields.ReverseRelation["Status"]
    user_1: User = fields.ReverseRelation["user_1"]
    user_2: User = fields.ReverseRelation["user_2"]
    reminder: List[Reminder] = fields.ReverseRelation["Reminder"]
    reminder_to: User = fields.ReverseRelation["reminder_to"]
    copypasta: List[Copypasta] = fields.ReverseRelation["Copypasta"]
    messages: List[MessagesLog] = fields.ReverseRelation["MessagesLog"]
    lottery: lottery = fields.ReverseRelation["Lottery"]
    imgur_aggregate: List[ImgurAggregate] = fields.ReverseRelation["ImgurAggregate"]
    imgur: List[Imgur] = fields.ReverseRelation["Imgur"]

    markov = fields.ReverseRelation["MarkovUsers"]
    markov_channels = fields.ReverseRelation["MarkovUserChannel"]

    translations: Translations = None


    class Meta:
        table = "user"

    def __str__(self) -> str:
        return f"{self.nickname}" if self.sponsor and self.nickname else f"@{self.name}"

    @property
    def timezone_(self):
        return ZoneInfo(self.timezone)


    @staticmethod
    async def create_or_update(ctx: Context) -> Optional[User]:
        if instance := await User.get_or_none(id=int(ctx.author.id)):
            return await User.update_user(instance, ctx)
        return await User.create_user(ctx)


    @staticmethod
    async def update_user(instance: User, ctx: Context) -> User:
        attrs = {
                "name": ctx.author.name,
                "channel": ctx.channel.name,
                "content": ctx.message.text.replace("ACTION", "", 1),
                "timestamp": ctx.message.timestamp,
        }
        update_fields = []

        if instance.name != ctx.author.name:
            await NickHistory.create(user=instance, nicks=instance.name)
        await User.log_message(instance, ctx)
        for attr, value in attrs.items():
            if attr == "content" and len(value) > 500:
                value = value[:500]
            if getattr(instance, attr) != value:
                setattr(instance, attr, value)
                update_fields.append(attr)

        if update_fields:
            update_fields.append("updated_at")
            await instance.save(update_fields=update_fields)

        return instance

    @staticmethod
    async def create_user(ctx: Context) -> User:
        user_data = {
                "id": ctx.author.id,
                "name": ctx.author.name,
                "channel": ctx.channel.name,
                "saved_color": ctx.author.colour,
                "content": ctx.message.text.replace("ACTION", "", 1),
                "timestamp": ctx.message.timestamp,
        }
        user = await User.create(**user_data)
        await NickHistory.create(user=user, nicks=user.name)
        await User.log_message(user, ctx)
        return user

    @staticmethod
    async def log_message(user: User, ctx: Context):
        message_type = "message_link" if URLExtract().find_urls(text=ctx.message.text) else "message"
        await MessagesLog.create(
                user=user,
                content=ctx.message.text[:500],
                type=message_type,
                channel=ctx.bot.channels[ctx.channel.name],
        )



    @staticmethod
    async def create_or_none(id: int, name: str, **kwargs) -> Optional[User]:
        if not await User.get_or_none(id=id):
            user = {
                    "id": id,
                    "name": name,
                    "channel": name,
                    "content": "",
                    "timestamp": 0,
                    **kwargs,
                    }
            user = await User.create(**user)
            await NickHistory.create(user=user, nicks=user.name)
            return user
        else:
            return None



class TwitchTokens(Base, TimestampMixin):
    user = fields.ForeignKeyField("models.User", related_name="TwitchTokens", unique=True)
    token = fields.CharField(max_length=255)
    refresh = fields.CharField(max_length=255)

    class Meta:
        table = "twitch_tokens"
