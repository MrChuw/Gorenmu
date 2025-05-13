from unittest.mock import MagicMock, patch

import pytest_asyncio


@pytest_asyncio.fixture(autouse=True)
async def silence_logging():
    with patch("logging.getLogger", return_value=MagicMock()):
        yield
