# -*- coding: utf-8 -*-

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


@pytest.mark.asyncio
async def test_count_no_name(interact, mock_context: MockContext):
    await mock_context.prepare_context("en")
    await Check.cookie_check(mock_context)
    response: Response = await interact.count._callback(interact, mock_context)
    assert (
        response.response_string == "you has 10 in stock. And has a total of 2 unredeemed."
    ), f"Expected 10 stock and 2 unredeemed, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_count_bot_name(interact, mock_context: MockContext):
    await mock_context.prepare_context("en")
    await Check.cookie_check(mock_context)
    args = [mock_context.bot.bot_nick]
    response: Response = await interact.count._callback(interact, mock_context, *args)
    assert (
        response.response_string == "I have infinite cookies, and I give away a fraction of them to you."
    ), f"Expected a sarcastic message, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_count_other_user(interact, mock_context: MockContext):
    await mock_context.prepare_context("en")
    await Check.cookie_check(mock_context)
    user = await User.get_user(mock_context, user_id=123456)
    await mock_context.create_cookie(user, received=25, consumed=54, donated=93, stocked=8534)
    args = [user.name]
    response: Response = await interact.count._callback(interact, mock_context, *args)
    assert response.response_string == (
        "@channelname has already eaten 54 cookies 🥠. Has 8534 in stock. "
        "Was presented with 25. Gifted 93. And has a total of 2 unredeemed."
    ), f"Expected a message with user cookie status, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_count_author_with_a_bunch_of_things(interact, mock_context: MockContext):
    await mock_context.prepare_context("en")
    await Check.cookie_check(mock_context)
    cookie = await Cookies.get(user=mock_context.user)
    cookie.received = 25
    cookie.consumed = 54
    cookie.donated = 93
    cookie.stocked = 8534
    await cookie.save()
    response: Response = await interact.count._callback(interact, mock_context)
    assert response.response_string == (
        "you have already eaten 54 cookies 🥠. Has 8534 in stock."
        " Was presented with 25. Gifted 93. And has a total of 2 unredeemed."
    ), f"Expected 10 stock and 2 unredeemed, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_count_user_not_found(interact, mock_context: MockContext):
    await mock_context.prepare_context("en")
    await Check.cookie_check(mock_context)
    args = ["random_user"]
    response: Response = await interact.count._callback(interact, mock_context, *args)
    assert (
        response.response_string
        == "user @random_user has not yet been registered and has not used any cookie commands."
    ), f"Expected a message with user cookie status, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response
