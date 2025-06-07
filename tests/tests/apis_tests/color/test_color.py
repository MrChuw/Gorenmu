# -*- coding: utf-8 -*-
import time
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from aiohttp_client_cache import CachedSession

from bot.apis import Color


@pytest.mark.asyncio
async def test_color_name_success():
    mock_response = AsyncMock()
    mock_response.json.return_value = {"name": {"value": "Cerulean"}, "hex": {"value": "#24B1E0"}}
    mock_get = AsyncMock(return_value=mock_response)
    async with CachedSession() as session:
        with patch.object(session, "get", mock_get):
            result = await Color.name({"hex": "24B1E0"}, session, MagicMock())
            assert result == "Cerulean", f"Expected 'Cerulean' from API, but got {result!r}"


@pytest.mark.asyncio
async def test_name_failure_returns_none():
    mock_response = AsyncMock()
    mock_response.json.return_value = {}
    mock_get = AsyncMock(side_effect=Exception("Error"))
    async with CachedSession() as session:
        with patch.object(session, "get", mock_get):
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
