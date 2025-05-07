# -*- coding: utf-8 -*-

import datetime

import pytest
import pytest_asyncio

from bot.cogs.cookies.command.cookies import CookieCmd
from tests.cogs.cookies.templates import templates_cookies_stock as templates
from tests.helpers.mock_classes import MockContext

lang = "pt_BR"


@pytest_asyncio.fixture
async def interact(mock_bot):
    return CookieCmd(bot=mock_bot)


@pytest.mark.asyncio
async def test_cookie_stock_on_cooldown(interact, mock_context: MockContext):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=1)]
    await templates.test_cookie_stock(
        interact,
        mock_context,
        lang=lang,
        content=[],
        expected="Você ainda está em cooldown, espere 60.00 segundos até o próximo lote! ⌛",
        values=values,
    )


@pytest.mark.asyncio
async def test_cookie_stock_no_content(interact, mock_context: MockContext):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=20)]
    await templates.test_cookie_stock(
        interact, mock_context, lang=lang, content=[], expected="você estocou 1 cookies 🍪.", values=values
    )


@pytest.mark.asyncio
async def test_cookie_stock_with_all(interact, mock_context: MockContext):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=20)]
    await templates.test_cookie_stock(
        interact,
        mock_context,
        lang=lang,
        content=["all"],
        expected="você estocou 4 cookies 🍪, o próximo sai em 6h.",
        values=values,
    )


@pytest.mark.asyncio
async def test_cookie_stock_with_amount(interact, mock_context: MockContext):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=20)]
    await templates.test_cookie_stock(
        interact, mock_context, lang=lang, content=["1"], expected="você estocou 1 cookies 🍪.", values=values
    )


@pytest.mark.asyncio
async def test_cookie_stock_with_exact_amount(interact, mock_context: MockContext):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=20)]
    await templates.test_cookie_stock(
        interact,
        mock_context,
        lang=lang,
        content=["4"],
        expected="você estocou 4 cookies 🍪, o próximo sai em 6h.",
        values=values,
    )


@pytest.mark.asyncio
async def test_cookie_stock_not_enough_cookies(interact, mock_context: MockContext):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=20)]
    await templates.test_cookie_stock(
        interact, mock_context, lang=lang, content=["6"], expected="você só pode estocar 4.", values=values
    )
