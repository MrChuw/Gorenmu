# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot.bot import Gorenmu

import pytest

from tests.helpers.mock_classes import MockContext


@pytest.mark.network
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "lang", [pytest.param("en", marks=pytest.mark.en, id="en"), pytest.param("pt", marks=pytest.mark.pt_BR, id="pt_BR")]
)
async def test_wikihow_real_session(mock_bot: Gorenmu, mock_context: MockContext, lang: str):
    session = mock_bot.SessionsCaches.WikihowCachedSession.session
    await mock_context.prepare_context(lang)
    main_url: str = mock_context.user.translations.Wikihow.url
    wiki = await mock_bot.SessionsCaches.WikihowCachedSession.get_not_cached(session, main_url)
    url = main_url.rsplit("/", 1)[0]
    assert wiki.status in [200, 304], f"Expected {repr([200, 304])}, got: {wiki.status!r}"
    assert url in wiki.url.human_repr(), f"Expected a {repr(url)} like url, got: {wiki.url.human_repr()!r}"
