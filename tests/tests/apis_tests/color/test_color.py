# -*- coding: utf-8 -*-
import time
from unittest.mock import MagicMock

import pytest
from aiohttp_client_cache import CachedSession

from bot.apis import Color
from tests.helpers.patches.patches import MockBuilder


@pytest.mark.asyncio
async def test_color_name_success():
    return_value = {"name": {"value": "Cerulean"}, "hex": {"value": "#24B1E0"}}
    async with CachedSession() as session:
        async with MockBuilder(None).Session.get_json(session, return_value):
            result = await Color.name({"hex": "24B1E0"}, session, MagicMock())
            assert result == "Cerulean", f"Expected 'Cerulean' from API, but got {result!r}"


@pytest.mark.asyncio
async def test_name_failure_returns_none():
    async with CachedSession() as session:
        async with MockBuilder(None).Session.get_json(session, side_effect=Exception("Error")):
            result = await Color.name({"hex": "24B1E0"}, session, MagicMock())
            assert result is None, f"Expected None due to API failure, but got {result!r}"


@pytest.mark.network
@pytest.mark.asyncio
async def test_name_real_session(mock_bot):
    session = mock_bot.tests_sessions.ColorSession.session
    result = await Color.name({"hex": "24B1E0"}, session, MagicMock())
    assert result == "Cerulean", f"Expected 'Cerulean' from real API, but got {result!r}"


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
