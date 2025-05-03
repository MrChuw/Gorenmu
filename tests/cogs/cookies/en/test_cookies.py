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


@pytest.mark.asyncio
async def test_cookie(interact, mock_context: MockContext):
    await mock_context.prepare_context("en")
    response: Response = await interact.cookies._callback(self=interact, ctx=mock_context)
    assert (
        response.response_string
        == 'Choose from one of the options "eat", "count", "top", "gift", "stock" or "sm"'
    ), f"Expected error message, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response
