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
    return MockContext("username", 12345, "channelname", 123456, mock_bot)  # NOQA


@pytest.mark.asyncio
async def test_rafk_not_in_time(interact, mock_context: MockContext):
    await mock_context.prepare_context('pt_BR')
    response: Response = await interact.rafk._callback(self=interact, ctx=mock_context)
    assert response.response_string == 'O tempo para retornar AFK já expirou.', \
        f"Expected a expired erro, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_rafk_with_content(interact, mock_context: MockContext):
    await mock_context.prepare_context('pt_BR')
    afk_str = {
            "content": "content",
            "updated_at": datetime.strptime("2025-01-01 06:00", "%Y-%m-%d %H:%M"),
            "alias": "afk"
    }

    await interact.bot.memcache.set(int(mock_context.author.id), afk_str, ttl=240, namespace="rafk")

    response: Response = await interact.rafk._callback(self=interact, ctx=mock_context)
    assert response.response_string == 'você continuou ausente 🏃⌨ e deixou uma nota: content', \
        f"Expected a return AFK message with emojis and content, got: {response.response_string!r}"


@pytest.mark.asyncio
async def test_rafk_no_content(interact, mock_context: MockContext):
    await mock_context.prepare_context('pt_BR')
    afk_str = {
            "content": "",
            "updated_at": datetime.strptime("2025-01-01 06:00", "%Y-%m-%d %H:%M"),
            "alias": "afk"
    }

    await interact.bot.memcache.set(int(mock_context.author.id), afk_str, ttl=240, namespace="rafk")

    response: Response = await interact.rafk._callback(self=interact, ctx=mock_context)
    assert response.response_string == 'você continuou ausente 🏃⌨', \
        f"Expected a return AFK message with emojis, got: {response.response_string!r}"
