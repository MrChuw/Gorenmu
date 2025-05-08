# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.cookies.command.cookies import CookieCmd
from tests.cogs.cookies.templates import templates_cookies as templates
from tests.helpers.mock_classes import MockContext

lang = "pt_BR"


@pytest_asyncio.fixture
async def interact(mock_bot):
    return CookieCmd(bot=mock_bot)


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_cookie(interact, mock_context: MockContext):
    await templates.test_cookie(
        interact,
        mock_context,
        lang=lang,
        content="",
        expected='Escolha entre uma das opções "eat", "count", "top", "gift", "stock" ou "sm"',
    )
