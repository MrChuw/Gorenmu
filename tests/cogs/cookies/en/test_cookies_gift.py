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


@pytest.mark.asyncio
async def test_cookie_gift_bot(interact, mock_context: MockContext):
    await mock_context.prepare_context("en")
    await Check.cookie_check(mock_context)
    args = [mock_context.bot.bot_nick]
    response: Response = await interact.gift._callback(interact, mock_context, *args)
    assert (
        response.response_string == "I don't want your cookie."
    ), f"Expected a sarcastic message, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_cookie_gift_yourself(interact, mock_context: MockContext):
    await mock_context.prepare_context("en")
    await Check.cookie_check(mock_context)
    args = [mock_context.author.name]
    response: Response = await interact.gift._callback(interact, mock_context, *args)
    assert (
        response.response_string == "Did you try gifting it yourself, wow!"
    ), f"Expected a sarcastic message, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_cookie_gift_unknown_user(interact, mock_context: MockContext):
    await mock_context.prepare_context("en")
    await Check.cookie_check(mock_context)
    args = ["random_user"]
    response: Response = await interact.gift._callback(interact, mock_context, *args)
    assert (
        response.response_string == "user @random_user has not yet been registered and "
        "has not used any cookie commands."
    ), f"Expected a error about not seen the user yet, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_cookie_gift_other_user_no_cookie(interact, mock_context: MockContext):
    await mock_context.prepare_context("en")
    await Check.cookie_check(mock_context)
    args = ["channelname"]
    response: Response = await interact.gift._callback(interact, mock_context, *args)
    assert (
        response.response_string == "User channelname has not yet used any command related to cookies."
    ), f"Expected a error about the user not using any cookie related command yet, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_cookie_gift_other_user_zero(interact, mock_context: MockContext):
    await mock_context.prepare_context("en")
    await Check.cookie_check(mock_context)
    user = await User.get_user(mock_context, user_id=123456)
    await mock_context.create_cookie(user, received=25, consumed=54, donated=93, stocked=8534)
    args = [user.name, "0"]
    response: Response = await interact.gift._callback(interact, mock_context, *args)
    assert (
        response.response_string == "You didn't gift anything, wow!"
    ), f"Expected a sarcastic message, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_cookie_gift_other_user_negative_amount(interact, mock_context: MockContext):
    await mock_context.prepare_context("en")
    await Check.cookie_check(mock_context)
    user = await User.get_user(mock_context, user_id=123456)
    await mock_context.create_cookie(user, received=25, consumed=54, donated=93, stocked=8534)
    args = [user.name, "-1"]
    response: Response = await interact.gift._callback(interact, mock_context, *args)
    assert (
        response.response_string == "You can't give negative cookies unless you're a cookie thief... "
        "and you're not, right?"
    ), f"Expected a sarcastic message, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_cookie_gift_cooldown_no_stock(interact, mock_context: MockContext):
    await mock_context.prepare_context("en")
    await Check.cookie_check(mock_context)
    user = await User.get_user(mock_context, user_id=123456)
    await mock_context.create_cookie(user, received=25, consumed=54, donated=93, stocked=8534)
    cookie = await Cookies.get_cookie(mock_context)
    cookie.stocked = 0
    cookie.cooldown = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)
    await cookie.save()
    args = [user.name]
    response: Response = await interact.gift._callback(interact, mock_context, *args)
    assert (
        "You don’t have any cookies 🍪 stored or waiting to be redeemed. The next one arrives in 59 minutes and"
        in response.response_string
    ), (
        f"Expected a message about not having stocked or unredeemed cookies + cooldown to next available, "
        f"got: {response.response_string!r}"
    )
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_cookie_gift_other_user_all(interact, mock_context: MockContext):
    await mock_context.prepare_context("en")
    await Check.cookie_check(mock_context)
    user = await User.get_user(mock_context, user_id=123456)
    await mock_context.create_cookie(user, received=25, consumed=54, donated=93, stocked=8534)
    args = [user.name, "all"]
    response: Response = await interact.gift._callback(interact, mock_context, *args)
    assert (
        response.response_string == "you gifted @channelname with 12 cookie 🎁"
    ), f"Expected user name and amount message, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_cookie_gift_other_user_no_amount(interact, mock_context: MockContext):
    await mock_context.prepare_context("en")
    await Check.cookie_check(mock_context)
    user = await User.get_user(mock_context, user_id=123456)
    await mock_context.create_cookie(user, received=25, consumed=54, donated=93, stocked=8534)
    args = [user.name]
    response: Response = await interact.gift._callback(interact, mock_context, *args)
    assert (
        response.response_string == "you gave @channelname a cookie 🎁"
    ), f"Expected user name message, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_cookie_gift_other_user_exact_amount(interact, mock_context: MockContext):
    await mock_context.prepare_context("en")
    await Check.cookie_check(mock_context)
    user = await User.get_user(mock_context, user_id=123456)
    await mock_context.create_cookie(user, received=25, consumed=54, donated=93, stocked=8534)
    args = [user.name, "10"]
    response: Response = await interact.gift._callback(interact, mock_context, *args)
    assert (
        response.response_string == "you gifted @channelname with 10 cookie 🎁"
    ), f"Expected user name and amount message, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_cookie_gift_other_user(interact, mock_context: MockContext):
    await mock_context.prepare_context("en")
    await Check.cookie_check(mock_context)
    user = await User.get_user(mock_context, user_id=123456)
    await mock_context.create_cookie(user, received=25, consumed=54, donated=93, stocked=8534)
    args = [user.name]
    response: Response = await interact.gift._callback(interact, mock_context, *args)
    assert (
        response.response_string == "you gave @channelname a cookie 🎁"
    ), f"Expected user name message, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_cookie_gift_other_user_no_stock_cooldown(interact, mock_context: MockContext):
    await mock_context.prepare_context("en")
    await Check.cookie_check(mock_context)
    user = await User.get_user(mock_context, user_id=123456)
    await mock_context.create_cookie(user, received=25, consumed=54, donated=93, stocked=8534)
    args = [user.name, "5"]
    response: Response = await interact.gift._callback(interact, mock_context, *args)
    assert (
        response.response_string == "you gifted @channelname with 5 cookie 🎁"
    ), f"Expected user name and amount message, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response

    response: Response = await interact.gift._callback(interact, mock_context, *args)
    assert (
        response.response_string == "you gifted @channelname with 5 cookie 🎁"
    ), f"Expected user name and amount message, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response

    response: Response = await interact.gift._callback(interact, mock_context, *args)
    assert (
        response.response_string == "To gift, you must first redeem the 2 cookies you have available."
    ), f"Expected a erro message with the amount of unredeemed cookies, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response
