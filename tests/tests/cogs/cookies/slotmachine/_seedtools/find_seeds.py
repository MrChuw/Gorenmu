# -*- coding: utf-8 -*-

import datetime

import pytest

from bot.translations import Response
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.cookies.slotmachine.test_slotmachine import mock_external_apis, prepare_cookie_context


async def base_find_seed(
    interact, mock_context: MockContext, lang: str, target_reward: int, bloco: int, emotes: bool = False
):
    step = 1000
    min_seed = bloco * step
    max_seed = min_seed + step

    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=24)]
    for seed in range(min_seed, max_seed):
        await prepare_cookie_context(mock_context, lang, seed, values)
        with mock_external_apis(emotes=emotes):
            response: Response = await interact.slotmachine._callback(interact, mock_context, amount="1")  # NOQA

        if f" {target_reward} " in response.response_string:
            print(f"\nHere is the seed: {seed}")
            assert f" {target_reward} " in response.response_string
            break
    else:
        print(f"\nSeed not found in block {bloco}")


@pytest.mark.asyncio
@pytest.mark.parametrize("lang", [pytest.param("en", id="en"), pytest.param("pt_BR", id="pt_BR")])
async def test_find_seed_for_reward_no_emotes(interact, mock_context: MockContext, lang: str):
    for i in range(20):
        found = await base_find_seed(interact, mock_context, lang=lang, target_reward=30, bloco=i)
        if found:
            print(f"Seed found in block {i}")
            return
    assert False


@pytest.mark.asyncio
@pytest.mark.parametrize("lang", [pytest.param("en", id="en"), pytest.param("pt_BR", id="pt_BR")])
async def test_find_seed_for_reward(interact, mock_context: MockContext, lang: str):
    for i in range(20):
        found = await base_find_seed(interact, mock_context, lang=lang, target_reward=30, bloco=i, emotes=True)
        if found:
            print(f"Seed found in block {i}")
            return
    assert False
