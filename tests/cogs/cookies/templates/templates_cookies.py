# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.cookies.command.cookies import CookieCmd
from bot.translations import Response
from tests.helpers.mock_classes import MockContext


@pytest_asyncio.fixture
async def interact(mock_bot):
    return CookieCmd(bot=mock_bot)


@pytest.fixture
def mock_context(mock_bot):
    return MockContext("username", 12345, "channelname", 123456, mock_bot)  # NOQA


@pytest.mark.template
@pytest.mark.asyncio
async def test_cookie(interact, mock_context: MockContext, lang: str, content: str, expected: str):
    await mock_context.prepare_context(lang)
    response: Response = await interact.cookies._callback(self=interact, ctx=mock_context)
    assert response.response_string == expected, f"Expected {expected!r}, got: {response.response_string!r}"
