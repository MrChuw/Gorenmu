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


@pytest.mark.template
@pytest.mark.asyncio
async def test_afk_return_not_afk(interact, mock_context: MockContext, lang: str, expected: bool):
    await mock_context.prepare_context(lang)
    response: Response | bool = await event_message(ctx=mock_context)
    assert response is expected, f"Expected {expected!r}, got: {response!r}"


@pytest.mark.template
@pytest.mark.asyncio
async def test_afk_return_afk_no_content(interact, mock_context: MockContext, lang: str, expected: str):
    await mock_context.prepare_context(lang)
    afk = (await Status.get_or_create(user=mock_context.user))[0]
    afk.updated_at = datetime.now(UTC)
    afk.alias = "afk"
    afk.online = False
    await afk.save()
    response: Response = await event_message(ctx=mock_context)
    assert (
        expected in response.response_string
    ), f"Expected {expected!r} to be in response.response_string, got: {response.response_string!r}"


@pytest.mark.template
@pytest.mark.asyncio
async def test_afk_return_afk_content(interact, mock_context: MockContext, lang: str, expected: str):
    await mock_context.prepare_context(lang)
    afk = (await Status.get_or_create(user=mock_context.user))[0]
    afk.updated_at = datetime.now(UTC)
    afk.alias = "afk"
    afk.message = "content"
    afk.online = False
    await afk.save()
    response: Response = await event_message(ctx=mock_context)
    assert (
        expected in response.response_string
    ), f"Expected {expected!r} to be in response.response_string, got: {response.response_string!r}"
