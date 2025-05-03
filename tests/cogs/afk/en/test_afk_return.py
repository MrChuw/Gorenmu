# -*- coding: utf-8 -*-

from datetime import datetime, UTC

import pytest
import pytest_asyncio

from bot.cogs.afk.commands.afk import AFKCmd
from bot.cogs.afk.manual_event_message.afk_return import event_message
from bot.models import Status
from bot.translations import Response
from tests.helpers.mock_classes import MockContext


@pytest_asyncio.fixture
async def interact(mock_bot):
    return AFKCmd(bot=mock_bot)


@pytest.fixture
def mock_context(mock_bot):
    return MockContext("username", 12345, "channelname", 123456, mock_bot)  # NOQA


@pytest.mark.asyncio
async def test_afk_return_not_afk(interact, mock_context: MockContext):
    await mock_context.prepare_context('en')
    response: Response | bool = await event_message(ctx=mock_context)
    assert response is False, f"Expected response to be False, got: {response!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_afk_return_afk_no_content(interact, mock_context: MockContext):
    await mock_context.prepare_context('en')
    afk = (await Status.get_or_create(user=mock_context.user))[0]
    afk.updated_at = datetime.now(UTC)
    afk.alias = "afk"
    afk.online = False
    await afk.save()
    response: Response = await event_message(ctx=mock_context)
    assert "you came back 🏃⌨ (was away for " in response.response_string, \
        f"Expected a return AFK message with emojis, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_afk_return_afk_content(interact, mock_context: MockContext):
    await mock_context.prepare_context('en')
    afk = (await Status.get_or_create(user=mock_context.user))[0]
    afk.updated_at = datetime.now(UTC)
    afk.alias = "afk"
    afk.message = "content"
    afk.online = False
    await afk.save()
    response: Response = await event_message(ctx=mock_context)
    assert "you came back 🏃⌨ and left a note: content (was away for" in response.response_string, \
        f"Expected a return AFK message with emojis with a note, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response
