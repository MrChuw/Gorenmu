# -*- ccookiesoding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.cookies.command.cookies import CookieCmd
from tests.tests.cogs.cookies.templates import templates_cookies as templates
from tests.helpers.mock_classes import MockContext

lang = "en"


@pytest_asyncio.fixture
async def interact(mock_bot):
    return CookieCmd(bot=mock_bot)


@pytest.mark.en
@pytest.mark.asyncio
async def test_cookie(interact, mock_context: MockContext):
    await templates.test_cookie(
        interact,
        mock_context,
        lang=lang,
        content="",
        expected='Choose from one of the options "eat", "count", "top", "gift", "stock" or "sm"',
    )
