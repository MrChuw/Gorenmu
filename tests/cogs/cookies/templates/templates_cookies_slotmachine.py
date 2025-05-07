# -*- coding: utf-8 -*-

import datetime
import re

import pytest
import pytest_asyncio
from aioresponses import aioresponses

from bot.cogs.cookies.command.cookies import CookieCmd
from bot.models import Cookies
from bot.translations import Response
from bot.utils import Check
from tests.helpers.mock_classes import MockContext


@pytest_asyncio.fixture
async def interact(mock_bot):
    return CookieCmd(bot=mock_bot)


@pytest.fixture
def mock_context(mock_bot):
    return MockContext("username", 12345, "channelname", 123456, mock_bot)  # NOQA


@pytest.mark.template
@pytest.mark.asyncio
async def test_cookie_slotmachine_no_emotes(
    interact,
    mock_context: MockContext,
    lang: str,
    content: str,
    values: list[int | datetime.datetime],
    seed: int = 0,
    expected: str | None = None,
    expected_regex: str | None = None,
):
    await mock_context.prepare_context(lang, seed)
    await Check.cookie_check(mock_context)
    cookie = await Cookies.get_cookie(mock_context)
    cookie.donated = values[0]
    cookie.stocked = values[1]
    cookie.received = values[2]
    cookie.consumed = values[3]
    cookie.cooldown = values[4]
    await cookie.save()
    with aioresponses() as mocked:
        mocked.get(re.compile(r".*"), payload={}, status=404)
        response: Response = await interact.slotmachine._callback(interact, mock_context, amount=content)
    if expected_regex:
        assert re.search(
            expected_regex, response.response_string
        ), f"Expected pattern {expected_regex!r}, got: {response.response_string!r}"
    elif expected:
        assert expected in response.response_string, f"Expected {expected!r}, got: {response.response_string!r}"
    else:
        raise ValueError("You must provide either `expected` or `expected_regex`.")


@pytest.mark.template
@pytest.mark.asyncio
async def test_cookie_slotmachine_emotes(
    interact,
    mock_context: MockContext,
    lang: str,
    content: str,
    values: list[int | datetime.datetime],
    seed: int = 0,
    expected: str | None = None,
    expected_regex: str | None = None,
):
    await mock_context.prepare_context(lang, seed)
    await Check.cookie_check(mock_context)
    cookie = await Cookies.get_cookie(mock_context)
    cookie.donated = values[0]
    cookie.stocked = values[1]
    cookie.received = values[2]
    cookie.consumed = values[3]
    cookie.cooldown = values[4]
    await cookie.save()
    payload = {
        "emote_set": {
            "emotes": [
                {"name": "GIGACHAD"},
                {"name": "NOOOO"},  # NOQA
                {"name": "ppPoof"},
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
    with aioresponses() as mocked:
        mocked.get(re.compile(r"https://7tv\.io/v3/users/twitch/.*"), payload=payload, status=200)
        mocked.get(re.compile(r"https://api\.betterttv\.net/.*"), payload={}, status=404)
        mocked.get(re.compile(r"https://api\.frankerfacez\.com/.*"), payload={}, status=404)
        response: Response = await interact.slotmachine._callback(interact, mock_context, amount=content)
    if expected_regex:
        assert re.search(
            expected_regex, response.response_string
        ), f"Expected pattern {expected_regex!r}, got: {response.response_string!r}"
    elif expected:
        assert expected in response.response_string, f"Expected {expected!r}, got: {response.response_string!r}"
    else:
        raise ValueError("You must provide either `expected` or `expected_regex`.")


@pytest.mark.template
@pytest.mark.asyncio
async def test_find_seed_for_reward_no_emotes(
    interact, mock_context: MockContext, lang: str, target_reward: int, bloco: int
):
    step = 1000
    min_seed = bloco * step
    max_seed = min_seed + step

    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=24)]
    for seed in range(min_seed, max_seed):
        await mock_context.prepare_context(lang, seed)
        await Check.cookie_check(mock_context)
        cookie = await Cookies.get_cookie(mock_context)
        cookie.donated = values[0]
        cookie.stocked = values[1]
        cookie.received = values[2]
        cookie.consumed = values[3]
        cookie.cooldown = values[4]
        await cookie.save()

        with aioresponses() as mocked:
            mocked.get(re.compile(r".*"), payload={}, status=404)
            response: Response = await interact.slotmachine._callback(interact, mock_context, amount="1")

        if f" {target_reward} " in response.response_string:
            print(f"\nHere is the seed: {seed}")
            assert f" {target_reward} " in response.response_string
            break
    else:
        print(f"\nSeed not found in block {bloco}")


@pytest.mark.template
@pytest.mark.asyncio
async def test_find_seed_for_reward_emotes(
    interact, mock_context: MockContext, lang: str, target_reward: int, bloco: int
) -> bool:
    step = 10_000
    min_seed = bloco * step
    max_seed = min_seed + step

    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=24)]
    for seed in range(min_seed, max_seed):
        await mock_context.prepare_context(lang, seed)
        await Check.cookie_check(mock_context)
        cookie = await Cookies.get_cookie(mock_context)
        cookie.donated = values[0]
        cookie.stocked = values[1]
        cookie.received = values[2]
        cookie.consumed = values[3]
        cookie.cooldown = values[4]
        await cookie.save()

        payload = {
            "emote_set": {
                "emotes": [
                    {"name": "GIGACHAD"},
                    {"name": "NOOOO"},  # NOQA
                    {"name": "ppPoof"},
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
        with aioresponses() as mocked:
            mocked.get(re.compile(r"https://7tv\.io/v3/users/twitch/.*"), payload=payload, status=200)
            mocked.get(re.compile(r"https://api\.betterttv\.net/.*"), payload={}, status=404)
            mocked.get(re.compile(r"https://api\.frankerfacez\.com/.*"), payload={}, status=404)
            response: Response = await interact.slotmachine._callback(interact, mock_context, amount="1")

        if f" {target_reward} " in response.response_string:
            print(f"\nHere is the seed: {seed}")
            print(f"\n{response.response_string!r}")
            return True
    print(f"\nSeed not found in block {bloco}")
    return False
