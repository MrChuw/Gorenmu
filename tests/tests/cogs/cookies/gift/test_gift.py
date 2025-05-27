# -*- coding: utf-8 -*-

import datetime

import pytest

from bot.cogs.cookies.command.cookies import CookieCmd
from bot.models import Cookies, User
from bot.translations import Response
from bot.utils import Check
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.cookies.gift.test_params import Params


async def prepare_and_create_cookie(mock_context: MockContext, lang, content, cookie_data=None):
    await mock_context.prepare_context(lang)
    await Check.cookie_check(mock_context)

    if cookie_data:
        user = await User.get_user(mock_context, name=content[0])
        await mock_context.create_cookie(user, **cookie_data)


async def call_and_assert(interact: CookieCmd, mock_context: MockContext, content, expected, index=None):
    response: Response = await interact.gift._callback(interact, mock_context, *content)  # NOQA
    if not index and isinstance(expected, list):
        assert (
            expected[0] in response.response_string
        ), f"Expected {expected[index]!r}, got: {response.response_string!r}"
    elif isinstance(expected, list):
        assert (
            expected[index] in response.response_string
        ), f"Expected {expected[index]!r}, got: {response.response_string!r}"
    else:
        assert response.response_string == expected, f"Expected {expected!r}, got: {response.response_string!r}"
    return response


async def base_gift(interact, mock_context: MockContext, lang: str, content: list[str], expected: str):
    await prepare_and_create_cookie(mock_context, lang, content)
    await call_and_assert(interact, mock_context, content, expected)


async def base_gift_user(
    interact, mock_context: MockContext, lang: str, content: list[str], expected: list[str], amount: int = 1
):
    cookie_data = dict(received=25, consumed=54, donated=93, stocked=8534)
    await prepare_and_create_cookie(mock_context, lang, content, cookie_data)
    for i in range(amount):
        await call_and_assert(interact, mock_context, content, expected, index=i)


async def base_user_edited(interact, mock_context: MockContext, lang: str, content: list[str], expected: str, values):
    await prepare_and_create_cookie(mock_context, lang, content, values)

    cookie = await Cookies.get_cookie(mock_context)
    cookie.donated = values["donated"]
    cookie.stocked = values["stocked"]
    cookie.received = values["received"]
    cookie.consumed = values["consumed"]
    cookie.cooldown = values["cooldown"]
    await cookie.save()

    await call_and_assert(interact, mock_context, content, expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.bot_nick)
async def test_bot_nick(interact, mock_context: MockContext, lang: str, expected: str | list[str]):
    await base_gift(interact, mock_context, lang=lang, content=[mock_context.bot.bot_nick], expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.yourself)
async def test_yourself(interact, mock_context: MockContext, lang: str, expected: str | list[str]):
    await base_gift(interact, mock_context, lang=lang, content=[mock_context.author.name], expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.unknown_user)
async def test_unknown_user(interact, mock_context: MockContext, lang: str, expected: str | list[str]):
    await base_gift(interact, mock_context, lang=lang, content=["random_user"], expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.other_user_no_cookie)
async def test_other_user_no_cookie(interact, mock_context: MockContext, lang: str, expected: str | list[str]):
    await base_gift(interact, mock_context, lang=lang, content=["channelname"], expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.other_user_zero)
async def test_other_user_zero(interact, mock_context: MockContext, lang: str, expected: str | list[str]):
    await base_gift_user(interact, mock_context, lang=lang, content=["channelname", "0"], expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.other_user_negative_amount)
async def test_other_user_negative_amount(interact, mock_context: MockContext, lang: str, expected: str | list[str]):
    await base_gift_user(interact, mock_context, lang=lang, content=["channelname", "-1"], expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.cooldown_no_stock)
async def test_cooldown_no_stock(interact, mock_context: MockContext, lang: str, expected: str | list[str]):
    values = dict(
        donated=10,
        stocked=0,
        received=10,
        consumed=10,
        cooldown=datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1),
    )
    await base_user_edited(
        interact, mock_context, lang=lang, content=["channelname", "1"], expected=expected, values=values
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.other_user_all)
async def test_other_user_all(interact, mock_context: MockContext, lang: str, expected: str | list[str]):
    await base_gift_user(interact, mock_context, lang=lang, content=["channelname", "all"], expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.other_user_no_amount)
async def test_other_user_no_amount(interact, mock_context: MockContext, lang: str, expected: str | list[str]):
    await base_gift_user(interact, mock_context, lang=lang, content=["channelname"], expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.other_user_exact_amount)
async def test_other_user_exact_amount(interact, mock_context: MockContext, lang: str, expected: str | list[str]):
    await base_gift_user(interact, mock_context, lang=lang, content=["channelname", "10"], expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.other_user)
async def test_other_user(interact, mock_context: MockContext, lang: str, expected: str | list[str]):
    await base_gift_user(interact, mock_context, lang=lang, content=["channelname"], expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.other_user_no_stock_cooldown)
async def test_other_user_no_stock_cooldown(interact, mock_context: MockContext, lang: str, expected: str | list[str]):
    await base_gift_user(interact, mock_context, lang=lang, content=["channelname", "5"], amount=3, expected=expected)
