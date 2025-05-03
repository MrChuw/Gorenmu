# -*- coding: utf-8 -*-
import datetime

import pytest
import pytest_asyncio

from bot.cogs.cookies.command.cookies import CookieCmd
from bot.models import Cookies
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
async def test_cookie_stock_on_cooldown(interact, mock_context: MockContext):
    await mock_context.prepare_context("en")
    await Check.cookie_check(mock_context)
    cookie = await Cookies.get_cookie(mock_context)
    cookie.cooldown = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=1)
    await cookie.save()
    args = []
    response: Response = await interact.stock._callback(interact, mock_context, *args)
    assert (
        response.response_string == "You're still on cooldown, wait 60.00 seconds until the next batch! ⌛"
    ), f"Expected message of cooldown, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_cookie_stock_no_content(interact, mock_context: MockContext):
    await mock_context.prepare_context("en")
    await Check.cookie_check(mock_context)
    args = []
    response: Response = await interact.stock._callback(interact, mock_context, *args)
    assert (
        response.response_string == "you stocked 1 cookies 🍪."
    ), f"Expected a message with one cookie, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_cookie_stock_with_all(interact, mock_context: MockContext):
    await mock_context.prepare_context("en")
    await Check.cookie_check(mock_context)
    args = ["all"]
    response: Response = await interact.stock._callback(interact, mock_context, *args)
    assert (
        response.response_string == "you stocked 2 cookies 🍪, the next one comes out in 6h."
    ), f"Expected a message with 2 cookies and the time util the next cookie, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_cookie_stock_with_amount(interact, mock_context: MockContext):
    await mock_context.prepare_context("en")
    await Check.cookie_check(mock_context)
    args = ["1"]
    response: Response = await interact.stock._callback(interact, mock_context, *args)
    assert (
        response.response_string == "you stocked 1 cookies 🍪."
    ), f"Expected a message with 1 cookie, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_cookie_stock_with_exact_amount(interact, mock_context: MockContext):
    await mock_context.prepare_context("en")
    await Check.cookie_check(mock_context)
    args = ["2"]
    response: Response = await interact.stock._callback(interact, mock_context, *args)
    assert (
        response.response_string == "you stocked 2 cookies 🍪, the next one comes out in 6h."
    ), f"Expected a message with 2 cookies and the time util the next cookie, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_cookie_stock_not_enough_cookies(interact, mock_context: MockContext):
    await mock_context.prepare_context("en")
    await Check.cookie_check(mock_context)
    args = ["4"]
    response: Response = await interact.stock._callback(interact, mock_context, *args)
    assert (
        response.response_string == "you can only stock 2 🍪."
    ), f"Expected a sarcastic message, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response
