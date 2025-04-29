# -*- coding: utf-8 -*-
import logging
import os
from unittest.mock import MagicMock, patch

import pytest_asyncio
import twitchio
from twitchio.web import StarletteAdapter

from bot.bot import Gorenmu
from bot.ext.config import Config
from tests.helpers.fake_db_data import create_fake_db


# @pytest_asyncio.fixture(autouse=True)
async def silence_logging():
    with patch("logging.getLogger", return_value=MagicMock()):
        yield


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
    await bot.setup_database()
    await create_fake_db(bot)

    yield bot

    await bot.SessionsCaches.close_all_sessions()
