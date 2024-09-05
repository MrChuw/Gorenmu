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

if TYPE_CHECKING:
    from bot.ext.commands import Context


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
    cookies: Coroutine[List[Cookies]] = fields.ReverseRelation["Cookies"]
    player: Coroutine[List[Player]] = fields.ReverseRelation["Player"]
    pets: Coroutine[List[Pets]] = fields.ReverseRelation["Pets"]
    player_torre: Coroutine[List[PlayerTower]] = fields.ReverseRelation["Player_torre"]
    suggest: Coroutine[List[Suggest]] = fields.ReverseRelation["Suggest"]
    bug: Coroutine[List[Bug]] = fields.ReverseRelation["Bug"]
    annotation: Coroutine[List[Annotation]] = fields.ReverseRelation["Annotation"]
    nick_history: Coroutine[List[Union[NickHistory, str]]] = fields.ReverseRelation["NickHistory"]
    status: Coroutine[List[Status]] = fields.ReverseRelation["Status"]
    user_1: User = fields.ReverseRelation["user_1"]
    user_2: User = fields.ReverseRelation["user_2"]
    reminder: Coroutine[List[Reminder]] = fields.ReverseRelation["Reminder"]
    reminder_to: User = fields.ReverseRelation["reminder_to"]
    copypasta: Coroutine[List[Copypasta]] = fields.ReverseRelation["Copypasta"]
    messages: Coroutine[List[MessagesLog]] = fields.ReverseRelation["MessagesLog"]
    lottery: lottery = fields.ReverseRelation["Lottery"]
    imgur_aggregate: Coroutine[List[ImgurAggregate]] = fields.ReverseRelation["ImgurAggregate"]
    imgur: Coroutine[List[Imgur]] = fields.ReverseRelation["Imgur"]

    markov = fields.ReverseRelation["MarkovUsers"]
    markov_channels = fields.ReverseRelation["MarkovUserChannel"]

    class Meta:
        table = "user"

    def __str__(self) -> str:
        return f"{self.nickname}" if self.sponsor and self.nickname else f"@{self.name}"

    @staticmethod
    async def create_or_update(ctx: Context, **kwargs) -> Optional[User]:
        if instance := await User.get_or_none(id=int(ctx.author.id)):
            attrs = {"name": ctx.author.name, "channel": ctx.channel.name,  # "saved_color": ctx.author.colour,
                     "content": ctx.message.content.replace("ACTION", "", 1), "timestamp": ctx.message.timestamp,
                     }
            update_fields = []
            if instance.name != ctx.author.name:
                await NickHistory.create(user=instance, nicks=instance.name)

            message_type = "message_link" if URLExtract().find_urls(text=ctx.message.content) else "message"
            await MessagesLog.create(user=instance, content=ctx.message.content[:500], type=message_type,
                                     channel=ctx.bot.channels[ctx.channel.name]
                                     )

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
        else:
            user = {"id": ctx.author.id, "name": ctx.author.name, "channel": ctx.channel.name,
                    "saved_color": ctx.author.colour, "content": ctx.message.content.replace("ACTION", "", 1),
                    "timestamp": ctx.message.timestamp, **kwargs,
                    }
            user = await User.create(**user)
            await NickHistory.create(user=user, nicks=user.name)
            message_type = "message_link" if URLExtract().find_urls(text=ctx.message.content) else "message"
            await MessagesLog.create(user=user, content=ctx.message.content[:500], type=message_type,
                                     channel=ctx.bot.channels[ctx.channel.name]
                                     )

            return user
