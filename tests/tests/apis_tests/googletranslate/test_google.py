# -*- coding: utf-8 -*-
import pytest

import bot.utils.cache_sessions
from bot.apis import GoogleTranslator


@pytest.mark.network
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "target, content, expected",
    [
        pytest.param("en", "Teste", "Test", marks=pytest.mark.en, id="en"),
        pytest.param("pt", "Test", "Teste", marks=pytest.mark.pt_BR, id="pt_BR"),
        pytest.param("es", "Test", "Prueba", marks=pytest.mark.es, id="es"),
    ],
)
async def test_translate_real_session(mock_bot, target: str, content: str, expected: str):
    session = bot.utils.cache_sessions.SessionsCaches.TranslateCachedSession.session
    translator = GoogleTranslator(session=session, target=target)
    result = await translator.translate(content)
    assert result == expected, f"Expected {expected!r}, but got {result!r}"
