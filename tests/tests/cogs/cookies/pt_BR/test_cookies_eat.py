# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.cookies.command.cookies import CookieCmd
from tests.tests.cogs.cookies.templates import templates_cookies_eat as templates
from tests.helpers.mock_classes import MockContext

lang = "pt_BR"


@pytest_asyncio.fixture
async def interact(mock_bot):
    return CookieCmd(bot=mock_bot)


@pytest.mark.pt_BR
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


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_cookie_eat_amount_zero(interact, mock_context: MockContext):
    await templates.test_cookie_eat(
        interact, mock_context, lang=lang, content=["0"], expected=["Você não comeu nada, nossa!"]
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_cookie_eat_amount_negative(interact, mock_context: MockContext):
    await templates.test_cookie_eat(
        interact,
        mock_context,
        lang=lang,
        content=["-1"],
        expected=["Para comer -1 cookies, você deve primeiro saber como reverter entropia."],
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_cookie_eat_multiple_amount(interact, mock_context: MockContext):
    await templates.test_cookie_eat(
        interact, mock_context, lang=lang, content=["2"], expected=["você comeu 2 cookies de uma só vez. 🥠"]
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_cookie_eat_cooldown(interact, mock_context: MockContext):
    expected = [
        "The person born with a talent they are meant to use will find their greatest happiness in using it.",
        "The trouble with most people is that they think with "
        "their hopes or fears or wishes rather than with their minds.",
        "Você ainda está em cooldown, espere 5 horas, 59 minutos e",
    ]
    await templates.test_cookie_eat(interact, mock_context, lang=lang, content=["1"], expected=expected, amount=3)
