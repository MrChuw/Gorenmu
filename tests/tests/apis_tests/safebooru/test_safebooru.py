from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot.bot import Gorenmu

import pytest

from bot.apis import booru


@pytest.mark.network
@pytest.mark.asyncio
async def test_safebooru_real_session(mock_bot: Gorenmu):
    session = mock_bot.SessionsCaches.Scp.session
    instance = booru.Booru().Safebooru(session=session)
    response = await instance.get(query="", page=1)
    expected = "https://safebooru.org/index.php?page=dapi&s=post&q=index&tags=&limit=100&pid=1&json=1"
    assert response.status == 200, f"Expected {200!r}, got: {response.status!r}"
    assert expected == response.url.human_repr(), f"Expected a {expected!r} url, got: {response.url.human_repr()!r}"
