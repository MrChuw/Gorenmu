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


@pytest.mark.asyncio
async def test_cookie_top_no_content(interact, mock_context: MockContext):
    await mock_context.prepare_context("en")
    await Check.cookie_check(mock_context)
    user = await User.get_user(mock_context, user_id=123456)
    await mock_context.create_cookie(user, received=25, consumed=54, donated=93, stocked=8534)
    args = []
    response: Response = await interact.top._callback(interact, mock_context, *args)
    assert (
        response.response_string == "the ranks are: stocked, streak, consumed, donated, received, total"
    ), f"Expected a error message with rank options, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_cookie_top_stocked(interact, mock_context: MockContext):
    await mock_context.prepare_context("en")
    await Check.cookie_check(mock_context)
    user = await User.get_user(mock_context, user_id=123456)
    await mock_context.create_cookie(user, received=25, consumed=54, donated=93, stocked=8534)
    args = ["stocked"]
    response: Response = await interact.top._callback(interact, mock_context, *args)
    assert (
        response.response_string
        == "top 5 stocked: 🏆 @channelname: (8534) 🥈 @some_user_45: (4185) 🥉 @some_user_44: (4092) "
        "🏅 @some_user_43: (3999) 🏅 @some_user_42: (3906) || "
        "You are in the 8th position in the ranking with 10."
    ), f"Expected the rank message, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_cookie_top_consumed(interact, mock_context: MockContext):
    await mock_context.prepare_context("en")
    await Check.cookie_check(mock_context)
    user = await User.get_user(mock_context, user_id=123456)
    await mock_context.create_cookie(user, received=25, consumed=54, donated=93, stocked=8534)
    args = ["consumed"]
    response: Response = await interact.top._callback(interact, mock_context, *args)
    assert (
        response.response_string
        == "top 5 cookiers: 🏆 @some_user_45: (3285) 🥈 @some_user_44: (3212) 🥉 @some_user_43: (3139) 🏅"
        " @some_user_42: (3066) 🏅 @some_user_41: (2993) || You are in the 8th position in the ranking with 0."
    ), f"Expected the rank message, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_cookie_top_donated(interact, mock_context: MockContext):
    await mock_context.prepare_context("en")
    await Check.cookie_check(mock_context)
    user = await User.get_user(mock_context, user_id=123456)
    await mock_context.create_cookie(user, received=25, consumed=54, donated=93, stocked=8534)
    args = ["donated"]
    response: Response = await interact.top._callback(interact, mock_context, *args)
    assert (
        response.response_string
        == "top 5 givers: 🏆 @some_user_45: (2520) 🥈 @some_user_44: (2464) 🥉 @some_user_43: (2408) "
        "🏅 @some_user_42: (2352) 🏅 @some_user_41: (2296) || You are in the 8th position in the ranking with 0."
    ), f"Expected the rank message, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_cookie_top_received(interact, mock_context: MockContext):
    await mock_context.prepare_context("en")
    await Check.cookie_check(mock_context)
    user = await User.get_user(mock_context, user_id=123456)
    await mock_context.create_cookie(user, received=25, consumed=54, donated=93, stocked=8534)
    args = ["received"]
    response: Response = await interact.top._callback(interact, mock_context, *args)
    assert (
        response.response_string
        == "top 5 receivers: 🏆 @some_user_45: (2430) 🥈 @some_user_44: (2376) 🥉 @some_user_43: (2322) "
        "🏅 @some_user_42: (2268) 🏅 @some_user_41: (2214) || You are in the 8th position in the ranking with 0."
    ), f"Expected the rank message, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_cookie_top_total(interact, mock_context: MockContext):
    await mock_context.prepare_context("en")
    await Check.cookie_check(mock_context)
    user = await User.get_user(mock_context, user_id=123456)
    await mock_context.create_cookie(user, received=25, consumed=54, donated=93, stocked=8534)
    args = ["total"]
    response: Response = await interact.top._callback(interact, mock_context, *args)
    assert (
        response.response_string
        == "top 5 total: 🏆 @some_user_40: (0) 🥈 @some_user_41: (0) 🥉 @some_user_42: (0) 🏅 @some_user_43: (0) "
        "🏅 @some_user_44: (0) || You are in the 1th position in the ranking with 0."
    ), f"Expected the rank message, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response
