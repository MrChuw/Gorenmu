# -*- coding: utf-8 -*-

import pytest

from bot.cogs.cookies.command.cookies import CookieCmd
from bot.translations import Response
from bot.utils import Check
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.cookies.eat.test_params import Params


async def base_eat(
    interact: CookieCmd, mock_context: MockContext, lang: str, content: list, expected: list[str], amount: int = 1
):
    await mock_context.prepare_context(lang)
    await Check.cookie_check(mock_context)
    for num in range(amount):
        response: Response = await interact.eat._callback(interact, mock_context, *content)  # NOQA
        assert (
            expected[num] in response.response_string
        ), f"Expected {expected[num]!r}, got: {response.response_string!r}"


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.with_nothing)
async def test_with_nothing(interact, mock_context: MockContext, lang: str, expected: list[str]):
    await base_eat(interact, mock_context, lang=lang, content=[], expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.amount_zero)
async def test_amount_zero(interact, mock_context: MockContext, lang: str, expected: list[str]):
    await base_eat(interact, mock_context, lang=lang, content=["0"], expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.amount_negative)
async def test_amount_negative(interact, mock_context: MockContext, lang: str, expected: list[str]):
    await base_eat(interact, mock_context, lang=lang, content=["-1"], expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.multiple_amount)
async def test_multiple_amount(interact, mock_context: MockContext, lang: str, expected: list[str]):
    await base_eat(interact, mock_context, lang=lang, content=["2"], expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.cooldown)
async def test_cooldown(interact, mock_context: MockContext, lang: str, expected: list[str]):
    await base_eat(interact, mock_context, lang=lang, content=["1"], amount=3, expected=expected)
