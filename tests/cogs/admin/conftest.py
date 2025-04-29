import pytest_asyncio
from unittest.mock import patch, MagicMock

@pytest_asyncio.fixture(autouse=True)
async def silence_logging():
    with patch("logging.getLogger", return_value=MagicMock()):
        yield
