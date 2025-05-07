# -*- coding: utf-8 -*-

import datetime
from unittest.mock import MagicMock, patch

import pytest
import pytest_asyncio

from bot.cogs.cookies.command.cookies import CookieCmd
from tests.cogs.cookies.templates import templates_cookies_slotmachine as templates
from tests.helpers.mock_classes import MockContext

lang = "pt_BR"


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


@pytest.mark.asyncio
async def test_slotmachine_on_cooldown(interact, mock_context: MockContext):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=1)]
    await templates.test_cookie_slotmachine_no_emotes(
        interact,
        mock_context,
        lang=lang,
        content="",
        expected_regex=r"Você ainda está em cooldown, espere \d+\.\d{2} segundos até o próximo lote! ⌛",
        values=values,
    )


@pytest.mark.asyncio
async def test_slotmachine_invalid_amount(interact, mock_context: MockContext):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(minutes=1)]
    await templates.test_cookie_slotmachine_no_emotes(
        interact,
        mock_context,
        lang=lang,
        content="amount",
        expected=" Você usou seu último cookie disponível e perdeu tudo. O próximo está disponível em 6 horas. PoroSad",
        values=values,
    )


@pytest.mark.asyncio
async def test_slotmachine_one_bunch_unredeemed(interact, mock_context: MockContext):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=24)]
    await templates.test_cookie_slotmachine_no_emotes(
        interact,
        mock_context,
        lang=lang,
        content="1",
        expected=" Você usou 1 cookie(s) não resgatado(s) e perdeu tudo.  PoroSad",
        values=values,
    )


@pytest.mark.asyncio
async def test_slotmachine_all_bunch_unredeemed(interact, mock_context: MockContext):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=24)]
    await templates.test_cookie_slotmachine_no_emotes(
        interact,
        mock_context,
        lang=lang,
        content="all",
        expected=" Você usou todos 5 cookie(s) não resgatado(s) e perdeu tudo. "
        "O próximo está disponível em 6 horas. PoroSad",
        values=values,
    )


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


@pytest.mark.asyncio
async def test_slotmachine_one_bunch_unredeemed_win_3(interact, mock_context: MockContext):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=24)]
    await templates.test_cookie_slotmachine_no_emotes(
        interact,
        mock_context,
        lang=lang,
        content="1",
        expected="[ 🍍 | 🍌 | 🍌 | 🍉 | 🍓 ] Você usou 1 cookie(s) não resgatado(s) e ganhou 3 cookies.  PogChamp",
        values=values,
        seed=2,
    )


@pytest.mark.asyncio
async def test_slotmachine_one_bunch_unredeemed_win_6(interact, mock_context: MockContext):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=24)]
    await templates.test_cookie_slotmachine_no_emotes(
        interact,
        mock_context,
        lang=lang,
        content="1",
        expected="[ 🥑 | 🍋 | 🍋 | 🍋 | 🍉 ] Você usou 1 cookie(s) não resgatado(s) e ganhou 6 cookies.  PogChamp",
        values=values,
        seed=15,
    )


@pytest.mark.asyncio
async def test_slotmachine_one_bunch_unredeemed_win_12(interact, mock_context: MockContext):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=24)]
    await templates.test_cookie_slotmachine_no_emotes(
        interact,
        mock_context,
        lang=lang,
        content="1",
        expected="[ 🍓 | 🍓 | 🍓 | 🍓 | 🍇 ] Você usou 1 cookie(s) não resgatado(s) e ganhou 12 cookies.  PogChamp",
        values=values,
        seed=651,
    )


@pytest.mark.asyncio
async def test_slotmachine_one_bunch_unredeemed_win_30(interact, mock_context: MockContext):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=24)]
    await templates.test_cookie_slotmachine_no_emotes(
        interact,
        mock_context,
        lang=lang,
        content="1",
        expected="[ 🍇 | 🍇 | 🍇 | 🍇 | 🍇 ] Você usou 1 cookie(s) não resgatado(s) e ganhou 30 cookies.  PogChamp",
        values=values,
        seed=120202,
    )


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


@pytest.mark.asyncio
async def test_slotmachine_one_bunch_unredeemed_win_3_emotes(interact, mock_context: MockContext):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=24)]
    await templates.test_cookie_slotmachine_emotes(
        interact,
        mock_context,
        lang=lang,
        content="1",
        expected="[ ppL | ppL | chuw | catJAM | 🍌 ] Você usou 1 cookie(s) não resgatado(s) e "
        "ganhou 3 cookies.  PogChamp",
        values=values,
        seed=2,
    )


@pytest.mark.asyncio
async def test_slotmachine_one_bunch_unredeemed_win_6_emotes(interact, mock_context: MockContext):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=24)]
    await templates.test_cookie_slotmachine_emotes(
        interact,
        mock_context,
        lang=lang,
        content="1",
        expected="[ papaoRun | papaoRun | papaoRun | 🥔 | COPIUM ] Você usou 1 cookie(s) não resgatado(s) "  # NOQA
        "e ganhou 6 cookies.  PogChamp",
        values=values,
        seed=15,
    )


@pytest.mark.asyncio
async def test_slotmachine_one_bunch_unredeemed_win_12_emotes(interact, mock_context: MockContext):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=24)]
    await templates.test_cookie_slotmachine_emotes(
        interact,
        mock_context,
        lang=lang,
        content="1",
        expected="[ GIGACHAD | GIGACHAD | GIGACHAD | GIGACHAD | NOOOO ] Você usou 1 cookie(s) não resgatado(s) "  # NOQA
        "e ganhou 12 cookies.  PogChamp",
        values=values,
        seed=1772,
    )


@pytest.mark.asyncio
async def test_slotmachine_one_bunch_unredeemed_win_30_emotes(interact, mock_context: MockContext):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=24)]
    await templates.test_cookie_slotmachine_emotes(
        interact,
        mock_context,
        lang=lang,
        content="1",
        expected="[ papaoRun | papaoRun | papaoRun | papaoRun | papaoRun ] Você usou 1 cookie(s) não resgatado(s) "  # NOQA
        "e ganhou 30 cookies.  PogChamp",
        values=values,
        seed=44296,
    )
