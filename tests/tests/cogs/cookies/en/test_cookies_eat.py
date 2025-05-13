# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.cookies.command.cookies import CookieCmd
from tests.tests.cogs.cookies.templates import templates_cookies_eat as templates
from tests.helpers.mock_classes import MockContext

lang = "en"


@pytest_asyncio.fixture
async def interact(mock_bot):
    return CookieCmd(bot=mock_bot)


@pytest.mark.en
@pytest.mark.asyncio
async def test_cookie_eat_with_nothing(interact, mock_context: MockContext):
    await templates.test_cookie_eat(
        interact,
        mock_context,
        lang=lang,
        content=[],
        expected=[
            "The person born with a talent they are meant to use will find their greatest happiness in using it."
        ],
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_cookie_eat_amount_zero(interact, mock_context: MockContext):
    await templates.test_cookie_eat(
        interact, mock_context, lang=lang, content=["0"], expected=["You didn't eat anything, wow!"]
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_cookie_eat_amount_negative(interact, mock_context: MockContext):
    await templates.test_cookie_eat(
        interact,
        mock_context,
        lang=lang,
        content=["-1"],
        expected=["To eat -1 cookies, you must first know how to reverse entropy."],
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_cookie_eat_multiple_amount(interact, mock_context: MockContext):
    await templates.test_cookie_eat(
        interact, mock_context, lang=lang, content=["2"], expected=["you ate 2 cookies in one sitting. 🥠"]
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_cookie_eat_cooldown(interact, mock_context: MockContext):
    expected = [
        "The person born with a talent they are meant to use will find their greatest happiness in using it.",
        "The trouble with most people is that they think with "
        "their hopes or fears or wishes rather than with their minds.",
        "You're still on cooldown, wait 5 hours, 59 minutes and",
    ]
    await templates.test_cookie_eat(interact, mock_context, lang=lang, content=["1"], expected=expected, amount=3)
