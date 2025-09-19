# -*- coding: utf-8 -*-

import datetime

import pytest

from bot.cogs.cookies.command.cookies import CookieCmd
from bot.ext import Response
from bot.models import Cookies, User
from bot.utils import Check
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.cookies.gift.test_params import Params


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    mock_context.Asserter.assert_string(interact.translations.Gift.deco_usage(mock_context, "+"), usage)
    mock_context.Asserter.assert_string(interact.translations.Gift.deco_helper(mock_context, "+"), helper)


async def prepare_and_create_cookie(mock_context: MockContext, lang, content, cookie_data=None, interact=None):
    await mock_context.prepare_context(lang)
    await Check.cookie_check(mock_context, interact.translations)

    if cookie_data:
        user = await User.get_user(mock_context, name=content[0], translations=interact.translations)
        await mock_context.create_cookie(user, **cookie_data)


async def call_and_assert(interact: CookieCmd, mock_context: MockContext, content, expected, success: bool, index=None):
    response: Response = await interact.gift._callback(interact, mock_context, *content)  # NOQA
    if isinstance(expected, list):
        selected = expected[0] if index is None else expected[index]
    else:
        selected = expected
    mock_context.Asserter.assert_string(response.response_string, selected)
    if success is not None:
        mock_context.Asserter.assert_boolean(response.success, success)


async def base_gift(
    interact, mock_context: MockContext, lang: str, content: list[str], expected: str, success: bool = False
):
    await prepare_and_create_cookie(mock_context, lang, content, None, interact)
    await call_and_assert(interact, mock_context, content, expected, success=success)


async def base_gift_user(
    interact,
    mock_context: MockContext,
    lang: str,
    content: list[str],
    expected: list[str],
    amount: int = 1,
    success: bool | None = False,
):
    cookie_data = dict(received=25, consumed=54, donated=93, stocked=8534)
    await prepare_and_create_cookie(mock_context, lang, content, cookie_data, interact)
    for i in range(amount):
        await call_and_assert(interact, mock_context, content, expected, index=i, success=success)


async def base_user_edited(
    interact, mock_context: MockContext, lang: str, content: list[str], expected: str, values, success: bool = False
):
    await prepare_and_create_cookie(mock_context, lang, content, values, interact)

    cookie = await Cookies.get_cookie(mock_context, interact.translations)
    cookie.donated = values["donated"]
    cookie.stocked = values["stocked"]
    cookie.received = values["received"]
    cookie.consumed = values["consumed"]
    cookie.cooldown = values["cooldown"]
    await cookie.save()

    await call_and_assert(interact, mock_context, content, expected, success=success)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.bot_nick)
async def test_bot_nick(interact, mock_context: MockContext, lang: str, expected: str | list[str]):
    await base_gift(
        interact, mock_context, lang=lang, content=[mock_context.bot.bot_nick], expected=expected, success=False
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.yourself)
async def test_yourself(interact, mock_context: MockContext, lang: str, expected: str | list[str]):
    await base_gift(
        interact, mock_context, lang=lang, content=[mock_context.author.name], expected=expected, success=False
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.unknown_user)
async def test_unknown_user(interact, mock_context: MockContext, lang: str, expected: str | list[str]):
    await base_gift(interact, mock_context, lang=lang, content=["random_user"], expected=expected, success=False)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.other_user_no_cookie)
async def test_other_user_no_cookie(interact, mock_context: MockContext, lang: str, expected: str | list[str]):
    await base_gift(interact, mock_context, lang=lang, content=["channelname"], expected=expected, success=False)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.other_user_zero)
async def test_other_user_zero(interact, mock_context: MockContext, lang: str, expected: str | list[str]):
    await base_gift_user(
        interact, mock_context, lang=lang, content=["channelname", "0"], expected=expected, success=False
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.other_user_negative_amount)
async def test_other_user_negative_amount(interact, mock_context: MockContext, lang: str, expected: str | list[str]):
    await base_gift_user(
        interact, mock_context, lang=lang, content=["channelname", "-1"], expected=expected, success=False
    )


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
        interact, mock_context, lang=lang, content=["channelname", "1"], expected=expected, values=values, success=False
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.other_user_all)
async def test_other_user_all(interact, mock_context: MockContext, lang: str, expected: str | list[str]):
    await base_gift_user(
        interact, mock_context, lang=lang, content=["channelname", "all"], expected=expected, success=True
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.other_user_no_amount)
async def test_other_user_no_amount(interact, mock_context: MockContext, lang: str, expected: str | list[str]):
    await base_gift_user(interact, mock_context, lang=lang, content=["channelname"], expected=expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.other_user_exact_amount)
async def test_other_user_exact_amount(interact, mock_context: MockContext, lang: str, expected: str | list[str]):
    await base_gift_user(
        interact, mock_context, lang=lang, content=["channelname", "10"], expected=expected, success=True
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.other_user)
async def test_other_user(interact, mock_context: MockContext, lang: str, expected: str | list[str]):
    await base_gift_user(interact, mock_context, lang=lang, content=["channelname"], expected=expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.other_user_no_stock_cooldown)
async def test_other_user_no_stock_cooldown(interact, mock_context: MockContext, lang: str, expected: str | list[str]):
    await base_gift_user(
        interact, mock_context, lang=lang, content=["channelname", "5"], amount=3, expected=expected, success=None
    )
