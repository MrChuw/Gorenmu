# -*- coding: utf-8 -*-
from __future__ import annotations

import random
import re
from typing import TYPE_CHECKING
from unittest.mock import AsyncMock, MagicMock

from twitchio.models import ChatMessage

from bot.models import Alias, Channel, Cookies, MessagesLog, User
from .Channel import MockChannel
from .User import MockUser

if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.translations import Response


class MockAuthor:
    def __init__(self, user_name: str, user_id):
        self.name = user_name
        self.display_name = user_name.capitalize()
        self.id = user_id
        self.is_mod = True
        self.is_subscriber = False
        self.colour = "#393993"


class MockMessage(MagicMock):
    def __init__(self, broadcaster: MockChannel, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timestamp = 11111111
        self.text = "Some Text"
        self.subscription_type = "chat.message"
        self.broadcaster = broadcaster
        self.user_input = "Some Text"


class MockContext(AsyncMock):
    def __init__(self, user_name: str, user_id: int, channel_name: str, channel_id: int, bot: Gorenmu):
        super().__init__()
        self.bot = bot
        self.user = MockUser(user_id, user_name)  # NOQA
        self.author = MockAuthor(user_name, user_id)
        self.channel = MockChannel(channel_id, channel_name)
        self.broadcaster = MockChannel(channel_id, channel_name)
        self.send = AsyncMock()
        self.reply = AsyncMock()
        self.resposta = AsyncMock()
        self.message = MockMessage(broadcaster=self.broadcaster, spec=ChatMessage)
        self.prefix = "+"

    async def prepare_context(self, translation: str = "en", seed: int = 0):
        random.seed(seed)
        self.user = await User.create_or_update(self)
        self.user.translations = self.bot.TranslationManager.get_translations(language=translation)

    async def prepare_alias(self, special_user):
        command_check = self.bot.get_command("chance")
        await Alias.create_cached(ctx=self, name="The_Tests_alias", command=command_check, invocation="chance")

        for num in range(45, 51):
            user = await self.bot.memcache.User.get(user_id=num)
            aliases_data = [
                (f"The_Tests_alias{num}", "chance", [""]),
                (f"The_Tests_alias{num+1}", "choice", ["1234", "123456", "|", "count", "{0}"]),
                (f"The_Tests_alias{num+2}", "upsidedown", ["upsidedown", "|", "count", "{0}"]),
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
    def assert_response(
        response: Response, expected: str | None = None, re_expected: str | None = None, strict: bool = False
    ):
        helper = f"Expected {(expected or re_expected)!r}, got: {response.response_string!r}"
        if re_expected:
            assert re.search(
                re_expected, response.response_string
            ), f"Expected pattern {re_expected!r}, got: {response.response_string!r}"
        elif expected:
            if strict:
                assert response.response_string == expected, helper
            else:
                assert expected in response.response_string, helper
        else:
            raise ValueError("You must provide either `expected` or `expected_regex`.")

    @staticmethod
    async def fake_messages():
        channel_user = await User.get(id=123456, name="channelname")
        channel = await Channel.get(user=channel_user)
        await MessagesLog.create(user=channel_user, content="Some Random Text", type="message", channel=channel)

        other_user = await User.get_or_none(id=12345)

        await MessagesLog.create(user=other_user, content="Some Random Text", type="message", channel=channel)
