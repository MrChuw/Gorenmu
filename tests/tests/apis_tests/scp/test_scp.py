from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot.bot import Gorenmu

import pytest

from bot.cogs.randomscp.command.randomscp import get_scp


@pytest.mark.network
@pytest.mark.asyncio
async def test_scp_real_session(mock_bot: Gorenmu):
    session = mock_bot.SessionsCaches.Scp.session
    scp = await get_scp(session)

    assert scp.status == 200, f"Expected {200!r}, got: {scp.status!r}"
    assert "https://scp-wiki.wikidot.com/" in scp.url.human_repr(), (
        f"Expected a {'https://scp-wiki.wikidot.com/'!r} like url, got: {scp.url.human_repr()!r}"
    )
