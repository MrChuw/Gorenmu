# -*- coding: utf-8 -*-

import contextlib
import datetime
import re
from unittest.mock import MagicMock, patch

import pytest
from aioresponses import aioresponses

from bot.models import Cookies
from bot.translations import Response
from bot.utils import Check
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.cookies.slotmachine.test_params import Params


# region Not need.


@pytest.fixture(autouse=True)
def silence_logs():
    with patch("logging.getLogger", return_value=MagicMock()):
        yield


def set_cookie_values(cookie, values: list[int | datetime.datetime]):
    cookie.donated = values[0]
    cookie.stocked = values[1]
    cookie.received = values[2]
    cookie.consumed = values[3]
    cookie.cooldown = values[4]


async def prepare_cookie_context(
    mock_context: MockContext, lang: str, seed: int, values: list[int | datetime.datetime] | None = None
):
    await mock_context.prepare_context(lang, seed)
    await Check.cookie_check(mock_context)
    if values:
        cookie = await Cookies.get_cookie(mock_context)
        set_cookie_values(cookie, values)
        await cookie.save()


@contextlib.contextmanager
def mock_external_apis(emotes: bool = True):
    with aioresponses() as mocked:
        mocked.get(re.compile(r"https://api\.betterttv\.net/.*"), payload={}, status=404)
        mocked.get(re.compile(r"https://api\.frankerfacez\.com/.*"), payload={}, status=404)
        if emotes:
            payload = {
                "emote_set": {
                    "emotes": [
                        {"name": "GIGACHAD"},
                        {"name": "NOOOO"},
                        {"name": "ppPoof"},  # NOQA
                        {"name": "modCheck"},
                        {"name": "catJAM"},
                        {"name": "Sadge"},
                        {"name": "Despair"},
                        {"name": "chuw"},
                        {"name": "AYAYA"},  # NOQA
                        {"name": "ppL"},
                        {"name": "Clueless"},
                        {"name": "COPIUM"},
                        {"name": "papaoRun"},  # NOQA
                    ]
                }
            }
            mocked.get(re.compile(r"https://7tv\.io/v3/users/twitch/.*"), payload=payload, status=200)
        else:
            mocked.get(re.compile(r"https://7tv\.io/v3/users/twitch/.*"), payload={}, status=404)
        yield mocked


# endregion


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    decorator = mock_context.bot.TranslationManager.get_decorator(interact.slotmachine, mock_context)
    mock_context.Asserter.assert_string(decorator.usage, usage)
    mock_context.Asserter.assert_string(decorator.helper, helper)


async def base_slotmachine(
    interact,
    mock_context: MockContext,
    lang: str,
    content: str,
    values: list | None = None,
    expected: str | None = None,
    re_expected: str | None = None,
    emotes: bool = True,
    seed: int = 0,
):
    await prepare_cookie_context(mock_context, lang, seed, values)
    with mock_external_apis(emotes=emotes):
        response: Response = await interact.slotmachine._callback(interact, mock_context, amount=content)  # NOQA

    mock_context.Asserter.assert_string(response.response_string, expected, re_expected)


# region Not need.


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.on_cooldown)
async def test_on_cooldown(interact, mock_context: MockContext, lang: str, expected: str):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=1)]
    await base_slotmachine(
        interact, mock_context, lang=lang, content="", re_expected=expected, values=values, emotes=False
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.invalid_amount)
async def test_invalid_amount(interact, mock_context: MockContext, lang: str, expected: str):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(minutes=1)]
    await base_slotmachine(
        interact, mock_context, lang=lang, content="amount", expected=expected, values=values, emotes=False
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.bunch_unredeemed_one)
async def test_bunch_unredeemed_one(interact, mock_context: MockContext, lang: str, expected: str):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=24)]
    await base_slotmachine(
        interact, mock_context, lang=lang, content="1", expected=expected, values=values, emotes=False
    )


# endregion


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.bunch_unredeemed_all)
async def test_bunch_unredeemed_all(interact, mock_context: MockContext, lang: str, expected: str):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=24)]
    await base_slotmachine(
        interact, mock_context, lang=lang, content="all", expected=expected, values=values, emotes=False
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.bunch_unredeemed_one_win_3)
async def test_bunch_unredeemed_one_win_3(interact, mock_context: MockContext, lang: str, expected: str):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=24)]
    await base_slotmachine(
        interact, mock_context, lang=lang, content="1", expected=expected, values=values, emotes=False, seed=2
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.bunch_unredeemed_one_win_6)
async def test_bunch_unredeemed_one_win_6(interact, mock_context: MockContext, lang: str, expected: str):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=24)]
    await base_slotmachine(
        interact, mock_context, lang=lang, content="1", expected=expected, values=values, emotes=False, seed=15
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.bunch_unredeemed_one_win_12)
async def test_bunch_unredeemed_one_win_12(interact, mock_context: MockContext, lang: str, expected: str):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=24)]
    await base_slotmachine(
        interact, mock_context, lang=lang, content="1", expected=expected, values=values, emotes=False, seed=651
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.bunch_unredeemed_one_win_30)
async def test_bunch_unredeemed_one_win_30(interact, mock_context: MockContext, lang: str, expected: str):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=24)]
    await base_slotmachine(
        interact, mock_context, lang=lang, content="1", expected=expected, values=values, emotes=False, seed=120202
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.bunch_unredeemed_one_win_3_emotes)
async def test_bunch_unredeemed_one_win_3_emotes(interact, mock_context: MockContext, lang: str, expected: str):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=24)]
    await base_slotmachine(
        interact, mock_context, lang=lang, content="1", expected=expected, values=values, emotes=True, seed=2
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.bunch_unredeemed_one_win_6_emotes)
async def test_bunch_unredeemed_one_win_6_emotes(interact, mock_context: MockContext, lang: str, expected: str):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=24)]
    await base_slotmachine(
        interact, mock_context, lang=lang, content="1", expected=expected, values=values, emotes=True, seed=15
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.bunch_unredeemed_one_win_12_emotes)
async def test_bunch_unredeemed_one_win_12_emotes(interact, mock_context: MockContext, lang: str, expected: str):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=24)]
    await base_slotmachine(
        interact, mock_context, lang=lang, content="1", expected=expected, values=values, emotes=True, seed=1772
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.bunch_unredeemed_one_win_30_emotes)
async def test_bunch_unredeemed_one_win_30_emotes(interact, mock_context: MockContext, lang: str, expected: str):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=24)]
    await base_slotmachine(
        interact, mock_context, lang=lang, content="1", expected=expected, values=values, emotes=True, seed=44296
    )
