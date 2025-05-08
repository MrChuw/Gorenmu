# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.cookies.command.cookies import CookieCmd
from tests.cogs.cookies.templates import templates_cookies_top as templates
from tests.helpers.mock_classes import MockContext

lang = "en"


@pytest_asyncio.fixture
async def interact(mock_bot):
    return CookieCmd(bot=mock_bot)


@pytest.mark.en
@pytest.mark.asyncio
async def test_cookie_top_no_content(interact, mock_context: MockContext):
    await templates.test_cookie_top(
        interact,
        mock_context,
        lang=lang,
        content=[],
        expected="the ranks are: stocked, streak, consumed, donated, received, total",
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_cookie_top_stocked(interact, mock_context: MockContext):
    await templates.test_cookie_top(
        interact,
        mock_context,
        lang=lang,
        content=["stocked"],
        expected="top 5 stocked: 🏆 @channelname: (8534) 🥈 @some_user_45: (4185) "
        "🥉 @some_user_44: (4092) 🏅 @some_user_43: (3999) 🏅 @some_user_42: "
        "(3906) || You are in the 8th position in the ranking with 10.",
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_cookie_top_consumed(interact, mock_context: MockContext):
    await templates.test_cookie_top(
        interact,
        mock_context,
        lang=lang,
        content=["consumed"],
        expected="top 5 cookiers: 🏆 @some_user_45: (3285) 🥈 @some_user_44: (3212) "
        "🥉 @some_user_43: (3139) 🏅 @some_user_42: (3066) 🏅 @some_user_41: "
        "(2993) || You are in the 8th position in the ranking with 0.",
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_cookie_top_donated(interact, mock_context: MockContext):
    await templates.test_cookie_top(
        interact,
        mock_context,
        lang=lang,
        content=["donated"],
        expected="top 5 givers: 🏆 @some_user_45: (2520) 🥈 @some_user_44: (2464) "
        "🥉 @some_user_43: (2408) 🏅 @some_user_42: (2352) 🏅 @some_user_41: "
        "(2296) || You are in the 8th position in the ranking with 0.",
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_cookie_top_received(interact, mock_context: MockContext):
    await templates.test_cookie_top(
        interact,
        mock_context,
        lang=lang,
        content=["received"],
        expected="top 5 receivers: 🏆 @some_user_45: (2430) 🥈 @some_user_44: (2376) "
        "🥉 @some_user_43: (2322) 🏅 @some_user_42: (2268) 🏅 @some_user_41: "
        "(2214) || You are in the 8th position in the ranking with 0.",
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_cookie_top_total(interact, mock_context: MockContext):
    await templates.test_cookie_top(
        interact,
        mock_context,
        lang=lang,
        content=["total"],
        expected="top 5 total: 🏆 @some_user_40: (0) 🥈 @some_user_41: (0) "
        "🥉 @some_user_42: (0) 🏅 @some_user_43: (0) 🏅 @some_user_44: "
        "(0) || You are in the 1th position in the ranking with 0.",
    )
