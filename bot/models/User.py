from __future__ import annotations

from typing import TYPE_CHECKING, Optional
from zoneinfo import ZoneInfo

from tortoise import fields

from bot.models.base import Base, ContentMixin, TimestampMixin
from bot.models.User_extras import MessagesLog, NickHistory
from bot.utils.string_manipulation import StringTools

if TYPE_CHECKING:
    from bot.ext import Context, TranslationBase
    from bot.models.User_extras import (
        Annotation,
        Bug,
        Cookies,
        Copypasta,
        Imgur,
        ImgurAggregate,
        Lottery,
        MarkovUserChannel,
        MarkovUsers,
        Pets,
        Player,
        PlayerTower,
        Reminder,
        Status,
        Suggest,
    )
    from bot.translations import Response

    GetReturnT = "User" | Response | None


class User(Base, TimestampMixin, ContentMixin):
    name: str = fields.CharField(unique=True, db_index=True, max_length=64, description="Twitch username")
    channel = fields.CharField(max_length=64, null=True, description="Twitch channel")
    saved_color = fields.CharField(max_length=7, null=True, description="Twitch color")
    city = fields.CharField(max_length=100, null=True)
    city_hidden = fields.BooleanField(default=True)
    ping = fields.BooleanField(default=True)
    mention = fields.BooleanField(default=True)
    block = fields.BooleanField(default=False)
    sponsor = fields.BooleanField(default=True)
    nickname = fields.CharField(max_length=32, null=True)
    timestamp = fields.DatetimeField(null=True)
    language = fields.CharField(max_length=32, null=True)
    timezone = fields.CharField(max_length=50, default="UTC")
    cookies: fields.ReverseRelation["Cookies"]
    player: fields.ReverseRelation["Player"]
    pets: fields.ReverseRelation["Pets"]
    player_torre: fields.ReverseRelation["PlayerTower"]
    suggest: fields.ReverseRelation["Suggest"]
    bug: fields.ReverseRelation["Bug"]
    annotation: fields.ReverseRelation["Annotation"]
    nick_history: fields.ReverseRelation["NickHistory"]
    status: fields.ReverseRelation["Status"]
    user_1: fields.ReverseRelation["User"]
    user_2: fields.ReverseRelation["User"]
    reminder: fields.ReverseRelation["Reminder"]
    reminder_to: fields.ReverseRelation["Reminder"]
    copypasta: fields.ReverseRelation["Copypasta"]
    messages: fields.ReverseRelation["MessagesLog"]
    lottery: fields.ReverseRelation["Lottery"]
    imgur_aggregate: fields.ReverseRelation["ImgurAggregate"]
    imgur: fields.ReverseRelation["Imgur"]

    markov: fields.ReverseRelation["MarkovUsers"]
    markov_channels: fields.ReverseRelation["MarkovUserChannel"]

    # translations: Translations = None
    user_id: int

    class Meta:
        table = "user"

    def __str__(self) -> str:
        return f"{self.nickname}" if self.sponsor and self.nickname else f"@{self.name}"

    @property
    def timezone_(self):
        return ZoneInfo(self.timezone)

    @staticmethod
    async def create_or_update(ctx: Context) -> Optional[User]:
        user = await ctx.bot.memcache.User.get(user_id=int(ctx.author.id))
        if not user:
            if instance := await User.get_or_none(id=int(ctx.author.id)):
                user = await User.update_user(instance, ctx)
            else:
                user = await User.create_user(ctx)
            await ctx.bot.memcache.User.set(user=user)
        else:
            await User.update_user(user, ctx)
        return user

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
            "content": ctx.message.text,
            "timestamp": ctx.message.timestamp,
        }
        user = await User.create(**user_data)
        await NickHistory.create(user=user, nicks=user.name)
        await User.log_message(user, ctx)
        return user

    @staticmethod
    async def log_message(user: User, ctx: Context):
        message_type = "message_link" if StringTools.urls_extract(ctx.message.text) else "message"
        await MessagesLog.create(
            user=user, content=ctx.message.text[:500], type=message_type, channel=ctx.bot.channels[ctx.channel.name]
        )

    @staticmethod
    async def create_or_none(user_id: int, name: str, **kwargs) -> Optional[User]:
        if not await User.get_or_none(id=user_id):
            user = {"id": user_id, "name": name, "channel": name, "content": "", "timestamp": 0, **kwargs}
            user = await User.create(**user)
            await NickHistory.create(user=user, nicks=user.name)
            return user
        else:
            return None

    @staticmethod
    async def find_by_name(name: str, ctx: Context, translations: TranslationBase, is_none: bool = False) -> GetReturnT:
        user = await ctx.bot.memcache.User.get_by_name(name=name)
        if not user:
            user = await User.get_or_none(name=name)
            if is_none and not user:
                return None
            if not user:
                return translations.Exceptions.user_not_found_name(ctx, name)
            await ctx.bot.memcache.User.set(user=user)
        return user

    @staticmethod
    async def find_by_id(
        user_id: int, ctx: Context, translations: TranslationBase, is_none: bool = False
    ) -> GetReturnT:
        user = await ctx.bot.memcache.User.get(user_id=user_id)
        if not user:
            user = await User.get_or_none(id=user_id)
            if is_none and not user:
                return None
            if not user:
                return translations.Exceptions.user_not_found_id(ctx, user_id)
            await ctx.bot.memcache.User.set(user=user)
        return user

    @staticmethod
    async def get_user(
        ctx: Context, translations: TranslationBase, name: str = None, user_id: int = None, is_none: bool = False
    ) -> GetReturnT:
        if name:
            return await User.find_by_name(name=name, ctx=ctx, is_none=is_none, translations=translations)
        elif user_id:
            return await User.find_by_id(user_id=user_id, ctx=ctx, is_none=is_none, translations=translations)
        else:
            return await User.find_by_id(user_id=ctx.user.id, ctx=ctx, is_none=is_none, translations=translations)

    @staticmethod
    async def get_user_or_none(
        ctx: Context, translations: TranslationBase, name: str = None, user_id: int = None
    ) -> GetReturnT:
        return await User.get_user(ctx, translations, name, user_id, is_none=True)


class TwitchTokens(Base, TimestampMixin):
    user = fields.ForeignKeyField("models.User", related_name="TwitchTokens", unique=True)
    token = fields.CharField(max_length=255)
    refresh = fields.CharField(max_length=255)

    class Meta:
        table = "twitch_tokens"
