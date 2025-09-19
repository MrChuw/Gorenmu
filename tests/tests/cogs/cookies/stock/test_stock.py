# -*- coding: utf-8 -*-

import datetime

import pytest

from bot.ext import Response
from bot.models import Cookies
from bot.utils import Check
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.cookies.stock.test_params import Params


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    mock_context.Asserter.assert_string(interact.translations.Stock.deco_usage(mock_context, "+"), usage)
    mock_context.Asserter.assert_string(interact.translations.Stock.deco_helper(mock_context, "+"), helper)


async def base_stock(
    interact,
    mock_context: MockContext,
    lang: str,
    content: list[str],
    values: list[int | datetime.datetime],
    expected: str | None = None,
    re_expected: str | None = None,
    success: bool = False,
):
    await mock_context.prepare_context(lang)
    await Check.cookie_check(mock_context, interact.translations)
    cookie = await Cookies.get_cookie(mock_context, interact.translations)
    cookie.donated = values[0]
    cookie.stocked = values[1]
    cookie.received = values[2]
    cookie.consumed = values[3]
    cookie.cooldown = values[4]
    await cookie.save()
    response: Response = await interact.stock._callback(interact, mock_context, *content)  # NOQA
    mock_context.Asserter.assert_string(response.response_string, expected, re_expected)
    mock_context.Asserter.assert_boolean(response.success, success)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.on_cooldown)
async def test_on_cooldown(interact, mock_context: MockContext, lang: str, expected: str):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=1)]
    await base_stock(interact, mock_context, lang=lang, content=[], re_expected=expected, values=values, success=False)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.no_content)
async def test_no_content(interact, mock_context: MockContext, lang: str, expected: str):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=20)]
    await base_stock(interact, mock_context, lang=lang, content=[], expected=expected, values=values, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.all)
async def test_all(interact, mock_context: MockContext, lang: str, expected: str):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=20)]
    await base_stock(interact, mock_context, lang=lang, content=["all"], expected=expected, values=values, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.with_amount)
async def test_with_amount(interact, mock_context: MockContext, lang: str, expected: str):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=20)]
    await base_stock(interact, mock_context, lang=lang, content=["1"], expected=expected, values=values, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.with_exact_amount)
async def test_with_exact_amount(interact, mock_context: MockContext, lang: str, expected: str):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=20)]
    await base_stock(
        interact, mock_context, lang=lang, content=["4"], re_expected=expected, values=values, success=True
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.not_enough_cookies)
async def test_not_enough_cookies(interact, mock_context: MockContext, lang: str, expected: str):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=20)]
    await base_stock(
        interact, mock_context, lang=lang, content=["6"], re_expected=expected, values=values, success=False
    )
