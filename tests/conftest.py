# -*- coding: utf-8 -*-
import logging
import os
from unittest.mock import MagicMock, patch
import asyncio

import contextlib
import pytest
import pytest_asyncio
import twitchio
from twitchio.web import StarletteAdapter

from bot.bot import Gorenmu
from bot.ext.config import Config
from tests.helpers.cached_sessions import SessionsCaches
from tests.helpers.fake_db_data import create_fake_db
from tests.helpers.mock_classes import MockContext


# @pytest_asyncio.fixture(autouse=True)
async def silence_logging():
    with patch("logging.getLogger", return_value=MagicMock()):
        yield


@pytest.fixture(autouse=True)
def silence_tortoise_logs():
    logging.getLogger("tortoise").setLevel(logging.WARNING)


@pytest.fixture
def mock_context(mock_bot):
    return MockContext("username", 12345, "channelname", 123456, mock_bot)  # NOQA


@pytest_asyncio.fixture
async def mock_bot():
    adapter: StarletteAdapter = StarletteAdapter(host="0.0.0.0")
    DEBUG = os.getenv("DEBUG", "1") == "1"  # NOQA
    Configs = Config(os.path.join(os.path.dirname(__file__), "test_config.toml"))  # NOQA

    if DEBUG:
        log = logging.getLogger()
        twitchio.utils.setup_logging(level=logging.INFO)
    else:
        from loguru import logger as log
        from bot.logger import InterceptHandler

        twitchio.utils.setup_logging(handler=InterceptHandler(), level=logging.INFO)
    bot = Gorenmu(configs=Configs, case_insensitive=True, log=log, adapter=adapter)
    bot.bot_nick = "bot_name"
    bot.dev_name = "dev_name"
    bot.tests_sessions = SessionsCaches(bot)
    await bot.setup_database()
    await bot.setup()
    await create_fake_db(bot)

    yield bot

    await bot.close()
    await bot.tests_sessions.close_all_sessions()
    bot.MarkovTask.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await bot.MarkovTask
    ...
