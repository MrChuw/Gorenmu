# -*- coding: utf-8 -*-
import random
import time

import pytest
import pytest_asyncio

from bot.apis import Emotes
from tests.helpers.patches.patches import MockBuilder

lang = "en"

ttv_payload = {
    "emote_set": {
        "emotes": [
            {"name": "GIGACHAD"},
            {"name": "NOOOO"},
            {"name": "ppPoof"},
            {"name": "modCheck"},
            {"name": "catJAM"},
        ]
    }
}

bttv_payload = {"channelEmotes": [{"code": "Sadge"}, {"code": "Despair"}, {"code": "chuw"}, {"code": "AYAYA"}]}

ffz_payload = {
    "room": {"set": "1010"},
    "sets": {"1010": {"emoticons": [{"name": "ppL"}, {"name": "Clueless"}, {"name": "COPIUM"}, {"name": "papaoRun"}]}},
}


@pytest_asyncio.fixture
async def interact(mock_bot):
    return Emotes(bot=mock_bot)


@pytest.mark.asyncio
async def test_7tv_success(interact):
    session = interact.bot.SessionsCaches.EmotesCachedSession.session
    async with MockBuilder(interact.bot).Session.get_json(session, ttv_payload):
        response = await interact.get_7tv(411010313)
        assert response == ["GIGACHAD", "NOOOO", "ppPoof", "modCheck", "catJAM"]


@pytest.mark.asyncio
async def test_7tv_404(interact):
    session = interact.bot.SessionsCaches.EmotesCachedSession.session
    async with MockBuilder(interact.bot).Session.get_json(session, ttv_payload, status=404):
        response = await interact.get_7tv(411010313)
        assert response == []


@pytest.mark.asyncio
async def test_bttv_success(interact):
    session = interact.bot.SessionsCaches.EmotesCachedSession.session
    async with MockBuilder(interact.bot).Session.get_json(session, bttv_payload):
        response = await interact.get_bttv(411010313)
        assert response == ["Sadge", "Despair", "chuw", "AYAYA"]


@pytest.mark.asyncio
async def test_bttv_404(interact):
    session = interact.bot.SessionsCaches.EmotesCachedSession.session
    async with MockBuilder(interact.bot).Session.get_json(session, bttv_payload, status=404):
        response = await interact.get_bttv(411010313)
        assert response == []


@pytest.mark.asyncio
async def test_ffz_success(interact):
    session = interact.bot.SessionsCaches.EmotesCachedSession.session
    async with MockBuilder(interact.bot).Session.get_json(session, ffz_payload):
        response = await interact.get_ffz(411010313)
        assert response == ["ppL", "Clueless", "COPIUM", "papaoRun"]


@pytest.mark.asyncio
async def test_ffz_404(interact):
    session = interact.bot.SessionsCaches.EmotesCachedSession.session
    async with MockBuilder(interact.bot).Session.get_json(session, ffz_payload, status=404):
        response = await interact.get_ffz(411010313)
        assert response == []


@pytest.mark.asyncio
async def test_fetch_emotes(interact):
    async with (
        MockBuilder(interact.bot)
        .Emotes.get_7tv(["GIGACHAD", "NOOOO", "ppPoof", "modCheck", "catJAM"])
        .Emotes.get_bttv(["Sadge", "Despair", "chuw", "AYAYA"])
        .Emotes.get_ffz(["ppL", "Clueless", "COPIUM", "papaoRun"])
    ):
        response = await interact.fetch_emotes(411010313)
        assert response == [
            "GIGACHAD",
            "NOOOO",
            "ppPoof",
            "modCheck",
            "catJAM",
            "Sadge",
            "Despair",
            "chuw",
            "AYAYA",
            "ppL",
            "Clueless",
            "COPIUM",
            "papaoRun",
        ]


@pytest.mark.asyncio
async def test_get_emotes(interact):
    async with (
        MockBuilder(interact.bot)
        .Emotes.get_7tv(["GIGACHAD", "NOOOO", "ppPoof", "modCheck", "catJAM"])
        .Emotes.get_bttv(["Sadge", "Despair", "chuw", "AYAYA"])
        .Emotes.get_ffz(["ppL", "Clueless", "COPIUM", "papaoRun"])
    ):
        response = await interact.get_emotes(411010313)
        assert response == [
            "GIGACHAD",
            "NOOOO",
            "ppPoof",
            "modCheck",
            "catJAM",
            "Sadge",
            "Despair",
            "chuw",
            "AYAYA",
            "ppL",
            "Clueless",
            "COPIUM",
            "papaoRun",
        ]


@pytest.mark.asyncio
async def test_get_emotes_cached(interact):
    async with (
        MockBuilder(interact.bot)
        .Emotes.get_7tv(["GIGACHAD", "NOOOO", "ppPoof", "modCheck", "catJAM"])
        .Emotes.get_bttv(["Sadge", "Despair", "chuw", "AYAYA"])
        .Emotes.get_ffz(["ppL", "Clueless", "COPIUM", "papaoRun"])
    ):
        response = await interact.fetch_emotes(411010313)
        assert response == [
            "GIGACHAD",
            "NOOOO",
            "ppPoof",
            "modCheck",
            "catJAM",
            "Sadge",
            "Despair",
            "chuw",
            "AYAYA",
            "ppL",
            "Clueless",
            "COPIUM",
            "papaoRun",
        ]
        response = await interact.get_emotes(411010313)
        assert response == [
            "GIGACHAD",
            "NOOOO",
            "ppPoof",
            "modCheck",
            "catJAM",
            "Sadge",
            "Despair",
            "chuw",
            "AYAYA",
            "ppL",
            "Clueless",
            "COPIUM",
            "papaoRun",
        ]


@pytest.mark.asyncio
async def test_get_emotes_random_by_amount_cached(interact):
    random.seed(411010313)
    async with (
        MockBuilder(interact.bot)
        .Emotes.get_7tv(["GIGACHAD", "NOOOO", "ppPoof", "modCheck", "catJAM"])
        .Emotes.get_bttv(["Sadge", "Despair", "chuw", "AYAYA"])
        .Emotes.get_ffz(["ppL", "Clueless", "COPIUM", "papaoRun"])
    ):
        response = await interact.get_random_by_amount(411010313, 1)
        assert response == ["Despair"]
        response = await interact.get_random_by_amount(411010313, 5)
        assert response == ["ppPoof", "papaoRun", "Despair", "modCheck", "ppL"]


@pytest.mark.network
@pytest.mark.asyncio
async def test_7tv_success_real_session(interact):
    response = await interact.get_7tv(411010313)
    assert response == ["GIGACHAD", "NOOOO", "catJAM", "COPIUM", "Sadge", "modCheck", "Clueless", "chuw", "Despair"]


@pytest.mark.network
@pytest.mark.asyncio
async def test_bttv_success_real_session(interact):
    response = await interact.get_bttv(411010313)
    assert response == ["papaoRun", "AYAYA", "ppPoof"]


@pytest.mark.network
@pytest.mark.asyncio
async def test_ffz_success_real_session(interact):
    response = await interact.get_ffz(411010313)
    assert response == ["ppL"]


@pytest.mark.network
@pytest.mark.asyncio
async def test_get_emotes_real_session(interact):
    response = await interact.get_emotes(411010313)
    assert response == [
        "GIGACHAD",
        "NOOOO",
        "catJAM",
        "COPIUM",
        "Sadge",
        "modCheck",
        "Clueless",
        "chuw",
        "Despair",
        "papaoRun",
        "AYAYA",
        "ppPoof",
        "ppL",
    ]


@pytest.mark.network
@pytest.mark.asyncio
async def test_get_emotes_cached_real_session(interact):
    response = await interact.get_emotes(411010313)
    assert response == [
        "GIGACHAD",
        "NOOOO",
        "catJAM",
        "COPIUM",
        "Sadge",
        "modCheck",
        "Clueless",
        "chuw",
        "Despair",
        "papaoRun",
        "AYAYA",
        "ppPoof",
        "ppL",
    ]

    start = time.perf_counter()
    response = await interact.get_emotes(411010313)
    elapsed = time.perf_counter() - start
    assert response == [
        "GIGACHAD",
        "NOOOO",
        "catJAM",
        "COPIUM",
        "Sadge",
        "modCheck",
        "Clueless",
        "chuw",
        "Despair",
        "papaoRun",
        "AYAYA",
        "ppPoof",
        "ppL",
    ]
    assert elapsed < 0.1, f"Expected: Basically instantaneous. But it took: {elapsed:.4f}s"
