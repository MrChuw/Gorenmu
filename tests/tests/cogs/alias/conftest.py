# -*- coding: utf-8 -*-
import pytest_asyncio

from bot.cogs.alias.command.alias import AliasCmd


@pytest_asyncio.fixture
async def interact(mock_bot):
    return AliasCmd(bot=mock_bot)
