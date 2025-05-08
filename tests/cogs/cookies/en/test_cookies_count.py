# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.cookies.command.cookies import CookieCmd
from tests.cogs.cookies.templates import templates_cookies_count as templates
from tests.helpers.mock_classes import MockContext

lang = "en"


@pytest_asyncio.fixture
async def interact(mock_bot):
    return CookieCmd(bot=mock_bot)


@pytest.mark.en
@pytest.mark.asyncio
async def test_count_no_name(interact, mock_context: MockContext):
    await templates.test_count(
        interact, mock_context, lang=lang, content=[], expected="you has 10 in stock. And has a total of 2 unredeemed."
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_count_bot_name(interact, mock_context: MockContext):
    await templates.test_count(
        interact,
        mock_context,
        lang=lang,
        content=[mock_context.bot.bot_nick],
        expected="I have infinite cookies, and I give away a fraction of them to you.",
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_count_other_user(interact, mock_context: MockContext):
    await templates.test_count_user(
        interact,
        mock_context,
        lang=lang,
        expected="@channelname has already eaten 54 cookies 🥠. Has 8534 in stock. "
        "Was presented with 25. Gifted 93. And has a total of 2 unredeemed.",
        use_target_user=True,
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_count_author_with_a_bunch_of_things(interact, mock_context: MockContext):
    await templates.test_count_user(
        interact,
        mock_context,
        lang=lang,
        expected="you have already eaten 54 cookies 🥠. "
        "Has 8534 in stock. Was presented with 25. Gifted 93. "
        "And has a total of 2 unredeemed.",
        use_target_user=False,
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_count_user_not_found(interact, mock_context: MockContext):
    await templates.test_count(
        interact,
        mock_context,
        lang=lang,
        content=["random_user"],
        expected="user @random_user has not yet been registered and has not used any cookie commands.",
    )
