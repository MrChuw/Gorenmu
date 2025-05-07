# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.cookies.command.cookies import CookieCmd
from bot.translations import Response
from bot.utils import Check
from tests.helpers.mock_classes import MockContext


@pytest_asyncio.fixture
async def interact(mock_bot):
    return CookieCmd(bot=mock_bot)


@pytest.fixture
def mock_context(mock_bot):
    return MockContext("username", 12345, "channelname", 123456, mock_bot)  # NOQA


@pytest.mark.template
@pytest.mark.asyncio
async def test_cookie_eat(
    interact, mock_context: MockContext, lang: str, content: list, expected: list[str], amount: int = 1
):
    await mock_context.prepare_context(lang)
    await Check.cookie_check(mock_context)
    for num in range(amount):
        response: Response = await interact.eat._callback(interact, mock_context, *content)
        assert (
            expected[num] in response.response_string
        ), f"Expected {expected[num]!r}, got: {response.response_string!r}"
