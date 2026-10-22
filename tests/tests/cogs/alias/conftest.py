import pytest_asyncio

from bot.cogs.alias.command.alias import AliasCmd


@pytest_asyncio.fixture
async def interact(mock_bot):
    await mock_bot.CommandHandler.load_cogs()
    return AliasCmd(bot=mock_bot)
