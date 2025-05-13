# -*- coding: utf-8 -*-

import datetime

import pytest
import pytest_asyncio

from bot.cogs.cookies.command.cookies import CookieCmd
from bot.models import Cookies, User
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
async def test_cookie_gift(interact, mock_context: MockContext, lang: str, content: list[str], expected: str):
    await mock_context.prepare_context(lang)
    await Check.cookie_check(mock_context)
    response: Response = await interact.gift._callback(interact, mock_context, *content)
    assert response.response_string == expected, f"Expected {expected!r}, got: {response.response_string!r}"


@pytest.mark.template
@pytest.mark.asyncio
async def test_cookie_gift_user(
    interact, mock_context: MockContext, lang: str, content: list[str], expected: list[str], amount: int = 1
):
    await mock_context.prepare_context(lang)
    await Check.cookie_check(mock_context)
    user = await User.get_user(mock_context, name=content[0])
    await mock_context.create_cookie(user, received=25, consumed=54, donated=93, stocked=8534)
    for num in range(amount):
        response: Response = await interact.gift._callback(interact, mock_context, *content)
        assert (
            expected[num] in response.response_string
        ), f"Expected {expected[num]!r}, got: {response.response_string!r}"


@pytest.mark.template
@pytest.mark.asyncio
async def test_cookie_gift_user_edited(
    interact,
    mock_context: MockContext,
    lang: str,
    content: list[str],
    expected: str,
    values: list[int | datetime.datetime],
):
    await mock_context.prepare_context(lang)
    await Check.cookie_check(mock_context)
    user = await User.get_user(mock_context, name=content[0])
    await mock_context.create_cookie(user, received=25, consumed=54, donated=93, stocked=8534)
    cookie = await Cookies.get_cookie(mock_context)
    cookie.donated = values[0]
    cookie.stocked = values[1]
    cookie.received = values[2]
    cookie.consumed = values[3]
    cookie.cooldown = values[4]
    await cookie.save()
    response: Response = await interact.gift._callback(interact, mock_context, *content)
    assert expected in response.response_string, f"Expected {expected!r}, got: {response.response_string!r}"
