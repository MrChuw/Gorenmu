# -*- coding: utf-8 -*-

from datetime import datetime

import pytest
import pytest_asyncio

from bot.cogs.afk.commands.rafk import RAfkCmd
from bot.translations import Response
from tests.helpers.mock_classes import MockContext


@pytest_asyncio.fixture
async def interact(mock_bot):
    return RAfkCmd(bot=mock_bot)


@pytest.fixture
def mock_context(mock_bot):
    return MockContext("username", 12345, "channelname", 123456, mock_bot)


@pytest.mark.asyncio
async def test_rafk_not_in_time(interact, mock_context: MockContext):
    await mock_context.prepare_context('en')
    response: Response = await interact.rafk._callback(self=interact, ctx=mock_context)
    assert response.response_string == 'Time to return AFK has already expired.'
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_rafk_with_content(interact, mock_context: MockContext):
    await mock_context.prepare_context('en')
    afk_str = {
            "content": "content",
            "updated_at": datetime.strptime("2025-01-01 06:00", "%Y-%m-%d %H:%M"),
            "alias": "afk"
    }

    await interact.bot.memcache.set(int(mock_context.author.id), afk_str, ttl=240, namespace="rafk")

    response: Response = await interact.rafk._callback(self=interact, ctx=mock_context)
    assert response.response_string == 'you continued afk 🏃⌨ and left a note: content'


@pytest.mark.asyncio
async def test_rafk_no_content(interact, mock_context: MockContext):
    await mock_context.prepare_context('en')
    afk_str = {
            "content": "",
            "updated_at": datetime.strptime("2025-01-01 06:00", "%Y-%m-%d %H:%M"),
            "alias": "afk"
    }
    await interact.bot.memcache.set(int(mock_context.author.id), afk_str, ttl=240, namespace="rafk")

    response: Response = await interact.rafk._callback(self=interact, ctx=mock_context)
    assert response.response_string == 'you continued afk 🏃⌨'
