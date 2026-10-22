from __future__ import annotations

import datetime
import random
from typing import TYPE_CHECKING
from unittest.mock import AsyncMock, MagicMock

from twitchio.models import ChatMessage
from twitchio.types_.eventsub import ChannelChatMessageEvent, ChatMessageData

from bot.ext import Context
from bot.models import Alias, Channel, Cookies, MessagesLog, User
from tests.helpers.patches.patches import MockBuilder

from .asserter import Asserter
from .channel import MockChannel
from .user import MockUser

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class MockAuthor(MagicMock):
    def __init__(
        self,
        name: str = "xxcoolnickxx",
        user_id: int = 1234567,
        display_name: str = "xXCoolNickXx",
        is_mod: bool = False,
        is_subscriber: bool = False,
        colour_hex: str = "393993",
    ):
        super().__init__()
        self.name = name
        self.display_name = display_name
        self.id = user_id
        self.is_mod = is_mod
        self.is_subscriber = is_subscriber

        self.colour = MagicMock()
        self.colour.hex_clean = colour_hex
        self.colour.hex = colour_hex

        self._http = MagicMock()


class MockMessage(MagicMock):
    def __init__(
        self,
        broadcaster: MockChannel,
        text: str = "Some Text",
        message_id: str = 'a2287bcfb0434bd7898b358183258a0a',
        timestamp: datetime.datetime | None = None,
        reply: str | None = None,
        badges: list | None = None,
        source_badges: list | None = None,
        message_type: str = "text",
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.timestamp = timestamp or datetime.datetime.now(datetime.UTC) - datetime.timedelta(milliseconds=1)
        self.text = text
        self.subscription_type = "chat.message"
        self.source_broadcaster = broadcaster
        self.broadcaster = broadcaster
        self.user_input = text
        self.reply = reply
        self.badges = badges
        self.source_badges = source_badges
        self.source_id = message_id
        self.id = message_id
        self.type = message_type
        self.cheer = None
        self.channel_points_animation_id = None


class MockContext(AsyncMock):
    def __init__(
        self,
        user_name: str,
        user_id: int | str,
        channel_name: str,
        channel_id: int | str,
        bot: Gorenmu,
        text: str = "Some Text",
        message_id: str = 'a2287bcfb0434bd7898b358183258a0a',
        timestamp: datetime.datetime | None = None,
        reply: str | None = None,
        badges: list | None = None,
        source_badges: list | None = None,
        message_type: str = "text",
    ):
        super().__init__(spec=Context)
        self.bot = bot
        self.prefix = "+"
        self.invoke_by = ""

        self.user = MockUser(name=user_name, user_id=int(user_id))
        self.author = MockAuthor(name=user_name, display_name=user_name, user_id=int(user_id))
        self.channel = MockChannel(channel_name=channel_name, channel_id=int(channel_id))
        self.broadcaster = self.channel
        self.author_display_name = self.author.name
        self.author_name = self.author.name
        self.channel_display_name = self.channel.name
        self.channel_name = self.channel.name
        self.bot_display_name = self.bot.bot_user.name or ""
        self.bot_name = self.bot.bot_user.name or ""
        self.dev_display_name = self.bot.dev_user.name or ""
        self.dev_name = self.bot.dev_user.name or ""

        self.message = MockMessage(
            broadcaster=self.broadcaster,
            text=text,
            message_id=message_id,
            timestamp=timestamp,
            reply=reply,
            badges=badges,
            source_badges=source_badges,
            message_type=message_type,
            spec=ChatMessage,
        )

        self.send = AsyncMock()
        self.reply = AsyncMock()
        self.resposta = AsyncMock()

        self.Asserter: Asserter = Asserter()
        self.MockBuilder: MockBuilder = MockBuilder(self)
        self.invoked_with: str = ""

    async def prepare_context(
        self, translation: str = "en", seed: int = 0, interact=None, afk_data=None, cookie_data=None, pet_data=None
    ):
        random.seed(seed)
        self.user = await User.create_or_update(self)
        self.user.language = translation

        if interact:
            interact.translations.ctx_set(self)
        if afk_data:
            from tests.helpers.fake_db_data import create_afk_data

            await create_afk_data(self.bot)
        if cookie_data:
            from tests.helpers.fake_db_data import create_cookie_db

            await create_cookie_db(self.bot)
        if pet_data:
            from tests.helpers.fake_db_data import create_pet_data

            await create_pet_data(self.bot)

    async def prepare_alias(self, special_user):
        command_check = self.bot.get_command("chance")
        if not command_check:
            return None
        await Alias.create_cached(ctx=self, name="The_Tests_alias", command=command_check, invocation="chance")

        for num in range(45, 51):
            user = await self.bot.memcache.User.get(user_id=num)
            aliases_data = [
                (f"The_Tests_alias{num}", "chance", [""]),
                (f"The_Tests_alias{num + 1}", "choice", ["1234", "123456", "|", "count", "{0}"]),
                (f"The_Tests_alias{num + 2}", "upsidedown", ["upsidedown", "|", "count", "{0}"]),
            ]
            for name, invocation, arguments in aliases_data:
                alias = Alias(
                    user_id=user.id,
                    channel_id=None,
                    name=name,
                    command=command_check.name,
                    invocation=invocation,
                    arguments=arguments,
                )
                await alias.save()
                await Alias.get_alias(ctx=self, user=user, name=name)

        if special_user:
            await Alias.create_cached(ctx=self, name="The_Tests_user", command=command_check, invocation="chance")

            user = User(name="The_Tests_user", display_name="The_Tests_user", language="en", id=54321)
            await user.save()

            alias = Alias(
                user_id=user.id,
                channel_id=None,
                name="The_Alias_test",
                command=command_check.name,
                invocation="chance",
                arguments=[""],
            )
            await alias.save()
            await Alias.get_alias(ctx=self, user=user, name="The_Alias_test")
            alias1 = Alias(
                user_id=user.id, channel_id=None, name="The_Alias_link", invocation="", arguments=[""], parent=alias
            )
            await alias1.save()
            await Alias.get_alias(ctx=self, user=user, name="The_Alias_link")
            alias2 = Alias(
                user_id=user.id,
                channel_id=None,
                name="The_Deleted_Alias_test",
                command="",
                invocation="",
                arguments=[""],
            )
            await alias2.save()
            await Alias.get_alias(ctx=self, user=user, name="The_Deleted_Alias_test")
            alias2 = Alias(
                user_id=user.id, name="The_Alias_link_link", command=None, invocation=None, arguments=[], parent=alias1
            )
            await alias2.save()
            await Alias.get_alias(ctx=self, user=user, name="The_Alias_link_link")

            await Alias.link_alias(ctx=self, name="The_Link_alias", parent=alias1)
            await Alias.get_alias(ctx=self, name="The_Link_alias")
            ...

    @staticmethod
    async def create_cookie(user, received=0, consumed=0, donated=0, stocked=0, cooldown=None):
        cookie = (await Cookies.get_or_create(user=user))[0]
        cookie.received = received
        cookie.consumed = consumed
        cookie.donated = donated
        cookie.stocked = stocked
        await cookie.save()
        await cookie.new_cooldown()
        if cooldown:
            cookie.cooldown = cooldown
            await cookie.save()
        return cookie

    @staticmethod
    async def fake_messages():
        channel_user = await User.get(id=123456, name="channelname")
        channel = await Channel.get(user=channel_user)
        await MessagesLog.create(user=channel_user, content="Some Random Text", type="message", channel=channel)

        other_user = await User.get_or_none(id=12345)

        await MessagesLog.create(user=other_user, content="Some Random Text", type="message", channel=channel)

    @classmethod
    def from_json(cls, data: dict, bot: Gorenmu | None = None):
        if bot is None:
            bot = MagicMock()

        user_name = data.get("loginName", "boring_nick")
        user_id = int(data.get("userID", "111024753"))
        channel_name = data.get("channelName", "pajlada")
        channel_id = int(data.get("channelID", "12345678"))

        badges = data.get("twitchBadges", [])
        is_mod = "moderator" in badges or "broadcaster" in badges
        is_subscriber = "subscriber" in badges

        raw_color = data.get("usernameColor", "#ffb22222")
        clean_color = raw_color.replace("#", "")
        if len(clean_color) == 8:
            clean_color = clean_color[2:]

        if raw_time := data.get("serverReceivedTime", ""):
            try:
                timestamp_obj = datetime.datetime.fromisoformat(raw_time).replace(tzinfo=datetime.UTC)
            except ValueError:
                timestamp_obj = None
        else:
            timestamp_obj = None

        ctx = cls(
            user_name=user_name,
            user_id=user_id,
            channel_name=channel_name,
            channel_id=channel_id,
            bot=bot,
            text=data.get("messageText", ""),
            message_id=data.get("id", ""),
            timestamp=timestamp_obj,
            reply=data.get("replyParent"),
            badges=badges,
            source_badges=data.get("externalBadges", []),
            message_type="text",
        )

        ctx.author.display_name = data.get("displayName", user_name)
        ctx.author.is_mod = is_mod
        ctx.author.is_subscriber = is_subscriber
        ctx.author.colour.hex_clean = clean_color

        return ctx
