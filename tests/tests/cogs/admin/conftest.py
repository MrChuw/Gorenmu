from unittest.mock import MagicMock, patch

import pytest_asyncio

from bot.cogs.admin.commands.admin import AdminSmallCmds


@pytest_asyncio.fixture(autouse=True)
async def silence_logging():
    with patch("logging.getLogger", return_value=MagicMock()):
        yield


@pytest_asyncio.fixture
async def interact(mock_bot):
    return AdminSmallCmds(bot=mock_bot)
