from __future__ import annotations

from typing import Coroutine, List, Union

from tortoise import fields

from bot.models.base import (
    Base, BoolFieldBool, CharFieldStr, ContentMixin, DatetimeTzField, TimestampMixin, UserMixin,
)
from bot.models.User_extras import (Annotation, Player, Cookies, NickHistory, Pets, Suggest, Bug,
                                    Status, Reminder, Copypasta, MessagesLog, Lottery, Imgur, ImgurAggregate,
                                    PlayerTower)


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
