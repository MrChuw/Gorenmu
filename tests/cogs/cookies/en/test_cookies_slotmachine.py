# -*- coding: utf-8 -*-

import datetime
from unittest.mock import MagicMock, patch

import pytest
import pytest_asyncio

from bot.cogs.cookies.command.cookies import CookieCmd
from tests.cogs.cookies.templates import templates_cookies_slotmachine as templates
from tests.helpers.mock_classes import MockContext

lang = "en"


@pytest_asyncio.fixture
async def interact(mock_bot):
    return CookieCmd(bot=mock_bot)


@pytest.fixture
def mock_context(mock_bot):
    return MockContext("username", 12345, "channelname", 411010313, mock_bot)  # NOQA


@pytest.fixture(autouse=True)
def silence_logs():
    with patch("logging.getLogger", return_value=MagicMock()):
        yield


@pytest.mark.en
@pytest.mark.asyncio
async def test_slotmachine_on_cooldown(interact, mock_context: MockContext):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=1)]
    await templates.test_cookie_slotmachine_no_emotes(
        interact,
        mock_context,
        lang=lang,
        content="",
        expected_regex=r"You're still on cooldown, wait \d+\.\d{2} seconds until the next batch! ⌛",
        values=values,
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_slotmachine_invalid_amount(interact, mock_context: MockContext):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(minutes=1)]
    await templates.test_cookie_slotmachine_no_emotes(
        interact,
        mock_context,
        lang=lang,
        content="amount",
        expected=" You used your last available cookie and lost everything. The next one is available in 6 hours.",
        values=values,
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_slotmachine_one_bunch_unredeemed(interact, mock_context: MockContext):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=24)]
    await templates.test_cookie_slotmachine_no_emotes(
        interact,
        mock_context,
        lang=lang,
        content="1",
        expected=" You have used 1 unredeemed cookie(s) and lost everything. ",
        values=values,
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_slotmachine_all_bunch_unredeemed(interact, mock_context: MockContext):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=24)]
    await templates.test_cookie_slotmachine_no_emotes(
        interact,
        mock_context,
        lang=lang,
        content="all",
        expected=" You have used all 5 unredeemed cookie(s) and lost everything. "
        "The next one is available in 6 hours.",
        values=values,
    )


@pytest.mark.en
@pytest.mark.template
@pytest.mark.asyncio
async def test_find_seed_for_reward_no_emotes(interact, mock_context: MockContext):
    for i in range(20):
        found = await templates.test_find_seed_for_reward_emotes(
            interact, mock_context, lang=lang, target_reward=30, bloco=i
        )
        if found:
            print(f"Seed found in block {i}")
            return
    assert False


@pytest.mark.en
@pytest.mark.asyncio
async def test_slotmachine_one_bunch_unredeemed_win_3(interact, mock_context: MockContext):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=24)]
    await templates.test_cookie_slotmachine_no_emotes(
        interact,
        mock_context,
        lang=lang,
        content="1",
        expected="[ 🍍 | 🍌 | 🍌 | 🍉 | 🍓 ] You have used 1 unredeemed cookie(s) and earned 3 cookies. ",
        values=values,
        seed=2,
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_slotmachine_one_bunch_unredeemed_win_6(interact, mock_context: MockContext):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=24)]
    await templates.test_cookie_slotmachine_no_emotes(
        interact,
        mock_context,
        lang=lang,
        content="1",
        expected="[ 🥑 | 🍋 | 🍋 | 🍋 | 🍉 ] You have used 1 unredeemed cookie(s) and earned 6 cookies. ",
        values=values,
        seed=15,
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_slotmachine_one_bunch_unredeemed_win_12(interact, mock_context: MockContext):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=24)]
    await templates.test_cookie_slotmachine_no_emotes(
        interact,
        mock_context,
        lang=lang,
        content="1",
        expected="[ 🍓 | 🍓 | 🍓 | 🍓 | 🍇 ] You have used 1 unredeemed cookie(s) and earned 12 cookies. ",
        values=values,
        seed=651,
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_slotmachine_one_bunch_unredeemed_win_30(interact, mock_context: MockContext):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=24)]
    await templates.test_cookie_slotmachine_no_emotes(
        interact,
        mock_context,
        lang=lang,
        content="1",
        expected="[ 🍇 | 🍇 | 🍇 | 🍇 | 🍇 ] You have used 1 unredeemed cookie(s) and earned 30 cookies. ",
        values=values,
        seed=120202,
    )


@pytest.mark.en
@pytest.mark.template
@pytest.mark.asyncio
async def test_find_seed_for_reward(interact, mock_context: MockContext):
    for i in range(20):
        found = await templates.test_find_seed_for_reward_emotes(
            interact, mock_context, lang=lang, target_reward=30, bloco=i
        )
        if found:
            print(f"Seed found in block {i}")
            return
    assert False


@pytest.mark.en
@pytest.mark.asyncio
async def test_slotmachine_one_bunch_unredeemed_win_3_emotes(interact, mock_context: MockContext):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=24)]
    await templates.test_cookie_slotmachine_emotes(
        interact,
        mock_context,
        lang=lang,
        content="1",
        expected="[ ppL | ppL | chuw | catJAM | 🍌 ] You have used 1 unredeemed cookie(s) and earned 3 cookies. ",
        values=values,
        seed=2,
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_slotmachine_one_bunch_unredeemed_win_6_emotes(interact, mock_context: MockContext):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=24)]
    await templates.test_cookie_slotmachine_emotes(
        interact,
        mock_context,
        lang=lang,
        content="1",
        expected="[ papaoRun | papaoRun | papaoRun | 🥔 | COPIUM ] "  # NOQA
        "You have used 1 unredeemed cookie(s) and earned 6 cookies. ",
        values=values,
        seed=15,
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_slotmachine_one_bunch_unredeemed_win_12_emotes(interact, mock_context: MockContext):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=24)]
    await templates.test_cookie_slotmachine_emotes(
        interact,
        mock_context,
        lang=lang,
        content="1",
        expected="[ GIGACHAD | GIGACHAD | GIGACHAD | GIGACHAD | NOOOO ] "  # NOQA
        "You have used 1 unredeemed cookie(s) and earned 12 cookies. ",
        values=values,
        seed=1772,
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_slotmachine_one_bunch_unredeemed_win_30_emotes(interact, mock_context: MockContext):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=24)]
    await templates.test_cookie_slotmachine_emotes(
        interact,
        mock_context,
        lang=lang,
        content="1",
        expected="[ papaoRun | papaoRun | papaoRun | papaoRun | papaoRun ] "  # NOQA
        "You have used 1 unredeemed cookie(s) and earned 30 cookies. ",
        values=values,
        seed=44296,
    )
