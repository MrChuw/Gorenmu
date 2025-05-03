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


@pytest.mark.asyncio
async def test_cookie_eat_with_nothing(interact, mock_context: MockContext):
    await mock_context.prepare_context("en")
    await Check.cookie_check(mock_context)
    response: Response = await interact.eat._callback(self=interact, ctx=mock_context)
    assert (
        response.response_string
        == "The person born with a talent they are meant to use will find their greatest happiness in using it."
    ), f"Expected a message with a phrase, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_cookie_eat_amount_zero(interact, mock_context: MockContext):
    await mock_context.prepare_context("en")
    await Check.cookie_check(mock_context)
    args = ["0"]
    response: Response = await interact.eat._callback(interact, mock_context, *args)
    assert (
        response.response_string == "You didn't eat anything, wow!"
    ), f"Expected a sarcastic message, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_cookie_eat_amount_negative(interact, mock_context: MockContext):
    await mock_context.prepare_context("en")
    await Check.cookie_check(mock_context)
    args = ["-1"]
    response: Response = await interact.eat._callback(interact, mock_context, *args)
    assert (
        response.response_string == "To eat -1 cookies, you must first know how to reverse entropy."
    ), f"Expected a sarcastic message, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_cookie_eat_multiple_amount(interact, mock_context: MockContext):
    await mock_context.prepare_context("en")
    await Check.cookie_check(mock_context)
    args = ["2"]
    response: Response = await interact.eat._callback(interact, mock_context, *args)
    assert (
        response.response_string == "you ate 2 cookies in one sitting. 🥠"
    ), f"Expected a sarcastic message, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_cookie_eat_cooldown(interact, mock_context: MockContext):
    await mock_context.prepare_context("en")
    await Check.cookie_check(mock_context)
    response: Response = await interact.eat._callback(self=interact, ctx=mock_context)
    assert (
        response.response_string
        == "The person born with a talent they are meant to use will find their greatest happiness in using it."
    ), f"Expected a message with a phrase, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response

    response: Response = await interact.eat._callback(self=interact, ctx=mock_context)
    assert (
        response.response_string == "The trouble with most people is that they think with their hopes or "
        "fears or wishes rather than with their minds."
    ), f"Expected a message with a phrase, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response

    response: Response = await interact.eat._callback(self=interact, ctx=mock_context)
    assert (
        "You're still on cooldown, wait 5 hours, 59 minutes and" in response.response_string
        and " seconds until the next batch! ⌛" in response.response_string
    ), f"Expected a message with a phrase, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response
