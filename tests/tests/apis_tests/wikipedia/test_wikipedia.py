from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot.bot import Gorenmu

import pytest
import pytest_asyncio

from bot.utils import SessionsCaches
from tests.helpers.mock_classes import MockContext


@pytest_asyncio.fixture
async def sessions(mock_bot):
    return SessionsCaches(mock_bot)


@pytest.mark.network
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "lang",
    [
        pytest.param("en", marks=pytest.mark.en, id="en"),
        pytest.param("pt", marks=pytest.mark.pt_BR, id="pt_BR"),
    ],
)
async def test_wikipedia_real_session(sessions, mock_bot: Gorenmu, mock_context: MockContext, lang: str):
    session = sessions.Wikipedia.session
    await mock_context.prepare_context(lang)
    main_url: str = mock_context.user.translations.Wikipedia.url
    wiki = await sessions.Wikipedia.get_not_cached(session, main_url)
    assert wiki.status == 200, f"Expected {200!r}, got: {wiki.status!r}"
