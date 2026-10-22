from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any, cast
from unittest.mock import AsyncMock

import twitchio
from twitchio import ChannelPointsRedemptionAdd, ChannelPointsRedemptionUpdate, ChatMessage, ChatMessageReply
from twitchio.ext.commands import Context as TwitchioContext

# Importe o tipo correto de onde a TwitchIO o define (geralmente twitchio.types.events ou similar)
from twitchio.types_.eventsub import ChannelChatMessageEvent
from twitchio.utils import Colour  # noqa

if TYPE_CHECKING:
    from twitchio.ext.commands.view import StringView

    from bot.bot import Gorenmu
    from bot.ext import Command, Response
    from bot.ext.commands import CustomComponent, Group
    from bot.models import User as UserModel


class Context(TwitchioContext):
    user: UserModel
    bot: Gorenmu
    command: Command | Group
    component: CustomComponent
    _command: Command  # type: ignore [bad-override-mutable-attribute]
    invoke_by: str
    reply_to: ChatMessageReply = None  # ty: ignore[invalid-assignment]

    def __init__(self, message: ChatMessage, *, bot: Gorenmu, prefix: str, invoke_by: str | None = None):
        super().__init__(message, bot=bot)
        if not invoke_by:
            invoke_by = ""
        self._prefix: str | None = prefix
        self.invoke_by: str = invoke_by
        if isinstance(self._payload, twitchio.Whisper):
            self.reply_to = None  # ty: ignore[invalid-assignment] # noqa
        else:
            self.reply_to = message.reply  # ty: ignore[invalid-assignment] # noqa

    @property
    def passed_guards(self) -> bool:
        return self._passed_guards

    def get_command(self):
        self._get_command()

    async def simple_response(self, ctx: Context, response: str | Response, handle: str | None = None) -> bool | None:
        if ctx.channel.name is None:
            return False

        if not ctx.bot.channels.is_online(ctx):
            return False
        response_str = response if isinstance(response, str) else response.response_string
        response_str, user_handler = await self.bot.ContextHandler.handle_banwords(ctx, response_str)

        if handle == "echo":
            return await self.bot.ContextHandler.handle_echo(ctx=ctx, response_str=response_str)
        return await self.bot.ContextHandler.send_response(ctx, user_handler, response_str)

    async def invoke(self) -> Response | bool:  # ty:ignore[invalid-method-override]
        return await self.bot.ContextHandler.invoke(self)

    @property
    def message(self) -> ChatMessage:  # | ChannelPointsRedemptionAdd | ChannelPointsRedemptionUpdate:
        """Property returning the :class:`~twitchio.ChatMessage` that this :class:`~.commands.Context` was
        created from. This could be ``None`` if :attr:`~.commands.Context.type` is :attr:`~.commands.ContextType.REWARD`
        """
        return (
            self._payload
        )  # if isinstance(self._payload, ChatMessage) else None  # ty: ignore[invalid-return-type]  # noqa

    @property
    def get_reply(self) -> ChatMessageReply | None:
        if isinstance(self.message, (ChannelPointsRedemptionAdd, ChannelPointsRedemptionUpdate)):
            return None
        return self.message.reply

    @property
    def view(self) -> StringView:
        return self._view

    @property
    def view_skip(self) -> StringView:
        view = self._view
        view.skip_ws()
        return view

    @property
    def prefix(self) -> str:
        return str(self._prefix)

    @property
    def author_display_name(self) -> str:
        return self.author.display_name or self.author.name or ""

    @property
    def author_name(self) -> str:
        return self.author.name or ""

    @property
    def author_colour(self) -> Colour | None:
        color = getattr(self.author, "color", None)
        return color if isinstance(color, Colour) else None

    @property
    def author_colour_hex(self) -> str | None:
        color = self.author_colour
        return color.hex if color else None

    @property
    def channel_display_name(self) -> str:
        return self.channel.display_name or self.channel.name or ""

    @property
    def channel_name(self) -> str:
        return self.channel.name or ""

    @property
    def bot_display_name(self) -> str:
        return self.bot.bot_user.display_name or self.bot.bot_user.name or ""

    @property
    def bot_name(self) -> str:
        return self.bot.bot_user.name or ""

    @property
    def dev_display_name(self) -> str:
        return self.bot.dev_user.display_name or self.bot.dev_user.name or ""

    @property
    def dev_name(self) -> str:
        return self.bot.dev_user.name or ""

    @classmethod
    def fake_payload(
        cls,
        *,
        content: str = "",
        user_id: str = "123456789",
        user_login: str = "fake_user",
        user_name: str = "Fake_User",
        broadcaster_id: str = "987654321",
        broadcaster_login: str = "fake_channel",
        broadcaster_name: str = "Fake_Channel",
        message_id: str | None = None,
        color: str = "#FFFFFF",
        message_type: str = "text",
        badges: list[dict] | None = None,
        reply: dict | None = None,
    ) -> ChannelChatMessageEvent:
        raw: dict[str, Any] = {
            "broadcaster_user_id": broadcaster_id,
            "broadcaster_user_login": broadcaster_login,
            "broadcaster_user_name": broadcaster_name,
            "chatter_user_id": user_id,
            "chatter_user_login": user_login,
            "chatter_user_name": user_name,
            "message_id": message_id or str(uuid.uuid4()),
            "message": {"text": content, "fragments": []},
            "color": color,
            "badges": badges or [],
            "message_type": message_type,
            "cheer": None,
            "reply": reply,
            "channel_points_custom_reward_id": None,
            "channel_points_animation_id": None,
            "source_broadcaster_user_id": None,
            "source_broadcaster_user_login": None,
            "source_broadcaster_user_name": None,
            "source_message_id": None,
            "source_badges": None,
            "is_source_only": None,
        }
        return cast(ChannelChatMessageEvent, raw)

    @classmethod
    def fake_ctx(
        cls,
        *,
        bot: Gorenmu,
        user: UserModel,
        channel_user: Any | None = None,
        channel_name: str = "fake_channel",
        content: str = "",
        message: ChatMessage | ChannelChatMessageEvent | None = None,
        prefix: str = "",
        invoke_by: str | None = None,
        timestamp: datetime | None = None,
    ) -> Context:
        user_id = str(getattr(user, "id", "123456789"))
        user_login = getattr(user, "login", getattr(user, "name", "fake_user")).lower()
        user_name = getattr(user, "nickname", None) or getattr(user, "name", "Fake_User")
        b_id = str(getattr(channel_user, "id", "987654321"))
        b_login = getattr(channel_user, "login", channel_name).lower()
        b_name = getattr(channel_user, "name", channel_name)

        now_ts = (timestamp or datetime.now(UTC)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        if isinstance(message, ChatMessage):
            chat_message = message
        else:
            raw_payload = message or cls.fake_payload(
                content=content,
                user_id=user_id,
                user_login=user_login,
                user_name=user_name,
                broadcaster_id=b_id,
                broadcaster_login=b_login,
                broadcaster_name=b_name,
            )

            chat_message = ChatMessage(raw_payload, http=bot._http)

            # Injeta diretamente o _metadata da BaseEvent para que chat_message.timestamp funcione
            chat_message._metadata = {
                "message_id": raw_payload["message_id"],
                "message_type": "notification",
                "message_timestamp": now_ts,
                "subscription_type": "channel.chat.message",
                "subscription_version": "1",
            }

        # Injeção para compatibilidade com discord_webhook
        if not hasattr(chat_message.chatter, "user"):
            mock_user = AsyncMock()
            mock_user.profile_image = AsyncMock()
            mock_user.profile_image.url = getattr(
                user,
                "profile_image_url",
                "https://static-cdn.jtvnw.net/user-default-pictures-uv/75305d54-c7cc-40d1-bbac-662c1140a348-profile_image-300x300.png",
            )
            chat_message.chatter.user = AsyncMock(return_value=mock_user)

        ctx = cls(
            message=chat_message,
            bot=bot,
            prefix=prefix,
            invoke_by=invoke_by,
        )
        ctx.user = user

        # Garante aliases exigidos pelo send_bug e discord_webhook
        if not hasattr(ctx, "author"):
            ctx.author = chat_message.chatter
        if not hasattr(ctx, "channel"):
            ctx.channel = chat_message.broadcaster

        return ctx

    async def is_enabled(self):
        return await self.bot.CommandHandler.is_enabled(self)

    async def is_online(self):
        return await self.bot.ChannelHandler.is_online(self)
