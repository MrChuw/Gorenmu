# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.cookies.command.cookies import CookieCmd
from bot.models import User
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
async def test_cookie_top(interact, mock_context: MockContext, lang: str, content: list[str], expected: str):
    await mock_context.prepare_context(lang)
    await Check.cookie_check(mock_context)
    user = await User.get_user(mock_context, user_id=123456)
    await mock_context.create_cookie(user, received=25, consumed=54, donated=93, stocked=8534)
    response: Response = await interact.top._callback(interact, mock_context, *content)
    assert response.response_string == expected, f"Expected {expected!r}, got: {response.response_string!r}"
