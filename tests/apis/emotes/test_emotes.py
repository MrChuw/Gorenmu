# -*- coding: utf-8 -*-

import pytest_asyncio
import time
from unittest.mock import MagicMock
from tests.helpers.mock_classes import MockContext

import pytest
from aiohttp_client_cache import CachedSession
from aioresponses import aioresponses

from bot.apis import Color
import re
from bot.apis import Emotes
import random

lang = "en"

ttv_payload = {
    "emote_set": {
        "emotes": [
            {"name": "GIGACHAD"},
            {"name": "NOOOO"},  # NOQA
            {"name": "ppPoof"},
            {"name": "modCheck"},
            {"name": "catJAM"},
        ]
    }
}

bttv_payload = {"channelEmotes": [{"code": "Sadge"}, {"code": "Despair"}, {"code": "chuw"}, {"code": "AYAYA"}]}  # NOQA

ffz_payload = {
    "room": {"set": 1010},
    "sets": {
        1010: {"emoticons": [{"name": "ppL"}, {"name": "Clueless"}, {"name": "COPIUM"}, {"name": "papaoRun"}]}  # NOQA
    },
}


# with aioresponses() as sdf:
#     mocked.get(re.compile(r"https://7tv\.io/v3/users/twitch/.*"), payload=ttv_payload, status=200)
#     mocked.get(re.compile(r"https://api\.betterttv\.net/.*"), payload=bttv_payload, status=404)
#     mocked.get(re.compile(r"https://api\.frankerfacez\.com/.*"), payload=ffz_payload, status=404)


@pytest_asyncio.fixture
async def interact(mock_bot):
    return Emotes(bot=mock_bot)


@pytest.mark.asyncio
async def test_7tv_success(interact):
    with aioresponses() as mocked:
        mocked.get(re.compile(r"https://7tv\.io/v3/users/twitch/.*"), payload=ttv_payload, status=200)
        response = await interact.get_7tv(411010313)
        assert response == ['GIGACHAD', 'NOOOO', 'ppPoof', 'modCheck', 'catJAM']  # NOQA


@pytest.mark.asyncio
async def test_7tv_404(interact):
    with aioresponses() as mocked:
        mocked.get(re.compile(r"https://7tv\.io/v3/users/twitch/.*"), payload=ttv_payload, status=404)
        response = await interact.get_7tv(411010313)
        assert response == []


@pytest.mark.asyncio
async def test_bttv_success(interact):
    with aioresponses() as mocked:
        mocked.get(re.compile(r"https://api\.betterttv\.net/.*"), payload=bttv_payload, status=200)
        response = await interact.get_bttv(411010313)
        assert response == ['Sadge', 'Despair', 'chuw', 'AYAYA']  # NOQA


@pytest.mark.asyncio
async def test_bttv_404(interact):
    with aioresponses() as mocked:
        mocked.get(re.compile(r"https://api\.betterttv\.net/.*"), payload=bttv_payload, status=404)
        response = await interact.get_bttv(411010313)
        assert response == []


@pytest.mark.asyncio
async def test_ffz_success(interact):
    with aioresponses() as mocked:
        mocked.get(re.compile(r"https://api\.frankerfacez\.com/.*"), payload=ffz_payload, status=200)
        response = await interact.get_ffz(411010313)
        assert response == ['ppL', 'Clueless', 'COPIUM', 'papaoRun']  # NOQA


@pytest.mark.asyncio
async def test_ffz_404(interact):
    with aioresponses() as mocked:
        mocked.get(re.compile(r"https://api\.frankerfacez\.com/.*"), payload=ffz_payload, status=404)
        response = await interact.get_ffz(411010313)
        assert response == []


@pytest.mark.asyncio
async def test_fetch_emotes(interact):
    with aioresponses() as mocked:
        mocked.get(re.compile(r"https://7tv\.io/v3/users/twitch/.*"), payload=ttv_payload, status=200)
        mocked.get(re.compile(r"https://api\.betterttv\.net/.*"), payload=bttv_payload, status=200)
        mocked.get(re.compile(r"https://api\.frankerfacez\.com/.*"), payload=ffz_payload, status=200)
        response = await interact.fetch_emotes(411010313)
        assert response == ['GIGACHAD', 'NOOOO', 'ppPoof', 'modCheck', 'catJAM', 'Sadge', 'Despair',  # NOQA
                            'chuw', 'AYAYA', 'ppL', 'Clueless', 'COPIUM', 'papaoRun']  # NOQA


@pytest.mark.asyncio
async def test_get_emotes(interact):
    with aioresponses() as mocked:
        mocked.get(re.compile(r"https://7tv\.io/v3/users/twitch/.*"), payload=ttv_payload, status=200)
        mocked.get(re.compile(r"https://api\.betterttv\.net/.*"), payload=bttv_payload, status=200)
        mocked.get(re.compile(r"https://api\.frankerfacez\.com/.*"), payload=ffz_payload, status=200)
        response = await interact.get_emotes(411010313)
        assert response == ['GIGACHAD', 'NOOOO', 'ppPoof', 'modCheck', 'catJAM', 'Sadge', 'Despair',  # NOQA
                            'chuw', 'AYAYA', 'ppL', 'Clueless', 'COPIUM', 'papaoRun']  # NOQA


@pytest.mark.asyncio
async def test_get_emotes_cached(interact):
    with aioresponses() as mocked:
        mocked.get(re.compile(r"https://7tv\.io/v3/users/twitch/.*"), payload=ttv_payload, status=200)
        mocked.get(re.compile(r"https://api\.betterttv\.net/.*"), payload=bttv_payload, status=200)
        mocked.get(re.compile(r"https://api\.frankerfacez\.com/.*"), payload=ffz_payload, status=200)
        response = await interact.fetch_emotes(411010313)
        assert response == ['GIGACHAD', 'NOOOO', 'ppPoof', 'modCheck', 'catJAM', 'Sadge', 'Despair',  # NOQA
                            'chuw', 'AYAYA', 'ppL', 'Clueless', 'COPIUM', 'papaoRun']  # NOQA
        response = await interact.get_emotes(411010313)
        assert response == ['GIGACHAD', 'NOOOO', 'ppPoof', 'modCheck', 'catJAM', 'Sadge', 'Despair',  # NOQA
                            'chuw', 'AYAYA', 'ppL', 'Clueless', 'COPIUM', 'papaoRun']  # NOQA


@pytest.mark.asyncio
async def test_get_emotes_random_by_amount_cached(interact):
    random.seed(411010313)
    with aioresponses() as mocked:
        mocked.get(re.compile(r"https://7tv\.io/v3/users/twitch/.*"), payload=ttv_payload, status=200)
        mocked.get(re.compile(r"https://api\.betterttv\.net/.*"), payload=bttv_payload, status=200)
        mocked.get(re.compile(r"https://api\.frankerfacez\.com/.*"), payload=ffz_payload, status=200)
        response = await interact.get_random_by_amount(411010313, 1)
        assert response == ['Despair']  # NOQA
        response = await interact.get_random_by_amount(411010313, 5)
        assert response == ['ppPoof', 'papaoRun', 'Despair', 'modCheck', 'ppL']  # NOQA


@pytest.mark.network
@pytest.mark.asyncio
async def test_7tv_success_real_session(interact):
    response = await interact.get_7tv(411010313)
    assert response == ['GIGACHAD', 'NOOOO', 'catJAM', 'COPIUM', 'Sadge', 'modCheck', 'Clueless', 'chuw', 'Despair']  # NOQA


@pytest.mark.network
@pytest.mark.asyncio
async def test_bttv_success_real_session(interact):
    response = await interact.get_bttv(411010313)
    assert response == ['papaoRun', 'AYAYA', 'ppPoof']  # NOQA


@pytest.mark.network
@pytest.mark.asyncio
async def test_ffz_success_real_session(interact):
    response = await interact.get_ffz(411010313)
    assert response == ['ppL']  # NOQA


@pytest.mark.network
@pytest.mark.asyncio
async def test_get_emotes_real_session(interact):
    response = await interact.get_emotes(411010313)
    assert response == ['GIGACHAD', 'NOOOO', 'catJAM', 'COPIUM', 'Sadge', 'modCheck', 'Clueless', 'chuw', 'Despair',  # NOQA
                        'papaoRun', 'AYAYA', 'ppPoof', 'ppL']  # NOQA


@pytest.mark.network
@pytest.mark.asyncio
async def test_get_emotes_cached_real_session(interact):
    response = await interact.get_emotes(411010313)
    assert response == ['GIGACHAD', 'NOOOO', 'catJAM', 'COPIUM', 'Sadge', 'modCheck', 'Clueless', 'chuw', 'Despair',  # NOQA
                        'papaoRun', 'AYAYA', 'ppPoof', 'ppL']  # NOQA

    start = time.perf_counter()
    response = await interact.get_emotes(411010313)
    elapsed = time.perf_counter() - start
    assert response == ['GIGACHAD', 'NOOOO', 'catJAM', 'COPIUM', 'Sadge', 'modCheck', 'Clueless', 'chuw', 'Despair',  # NOQA
                        'papaoRun', 'AYAYA', 'ppPoof', 'ppL']  # NOQA
    assert elapsed < 0.1, f"Expected: Basically instantaneous. But it took: {elapsed:.4f}s"


@pytest.mark.network
@pytest.mark.asyncio
async def test_name_real_session_cached(mock_bot):
    session = mock_bot.tests_sessions.ColorSession.session

    result1 = await Color.name({"hex": "24B1E0"}, session, MagicMock())
    assert result1 == "Cerulean", f"Expected 'Cerulean' from real API, but got {result1!r}"

    start = time.perf_counter()
    result2 = await Color.name({"hex": "24B1E0"}, session, MagicMock())
    elapsed = time.perf_counter() - start

    assert result2 == "Cerulean", f"Expected 'Cerulean' from real API, but got {result2!r}"
    assert elapsed < 0.1, f"Expected: Basically instantaneous. But it took: {elapsed:.4f}s"
