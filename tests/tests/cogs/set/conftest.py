import pytest_asyncio

from bot.cogs.set.command.set import SetCmd


@pytest_asyncio.fixture
async def interact(mock_bot):
    return SetCmd(bot=mock_bot)
