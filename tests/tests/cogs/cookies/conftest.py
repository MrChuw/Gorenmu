# -*- coding: utf-8 -*-

import pytest_asyncio

from bot.cogs.cookies.command.cookies import CookieCmd


@pytest_asyncio.fixture
async def interact(mock_bot):
    return CookieCmd(bot=mock_bot)
