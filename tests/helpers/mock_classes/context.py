# -*- coding: utf-8 -*-
from __future__ import annotations

import random
from typing import TYPE_CHECKING
from unittest.mock import AsyncMock

from bot.models import Cookies, User
from .Channel import MockChannel
from .User import MockUser

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class MockAuthor:
    def __init__(self, user_name: str, user_id):
        self.name = user_name
        self.display_name = user_name.capitalize()
        self.id = user_id
        self.is_mod = True
        self.is_subscriber = False
        self.colour = "#393993"


class MockMessage:
    def __init__(self):
        self.timestamp = 11111111
        self.text = "Some Text"


class MockContext(AsyncMock):
    def __init__(self, user_name: str, user_id: int, channel_name: str, channel_id: int, bot: Gorenmu):
        super().__init__()
        self.bot = bot
        self.user = MockUser(user_id, user_name)
        self.author = MockAuthor(user_name, user_id)
        self.channel = MockChannel(channel_id, channel_name)
        self.broadcaster = MockChannel(channel_id, channel_name)
        self.send = AsyncMock()
        self.reply = AsyncMock()
        self.resposta = AsyncMock()
        self.message = MockMessage()

    async def prepare_context(self, translation: str = 'en'):
        random.seed(0)
        self.user = await User.create_or_update(self)
        self.user.translations = self.bot.TranslationManager.get_translations(language=translation)
        ...

    async def create_cookie(self, user, received=0, consumed=0, donated=0, stocked=0):
        cookie = await Cookies.create(user=user)
        cookie.received = received
        cookie.consumed = consumed
        cookie.donated = donated
        cookie.stocked = stocked
        await cookie.save()
        await cookie.new_cooldown()
        return cookie
