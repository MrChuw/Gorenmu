import asyncio
import logging
import os

import twitchio
import uvloop
from twitchio.web import StarletteAdapter

# from bot.api import api, api_start
from bot.bot import Gorenmu
from bot.utils.config import Config

Configs = Config(os.path.join(os.path.dirname(__file__), "config.toml"))

if os.getenv("NO_LOG") == "1":
    import logging

    log = logging.getLogger()
    twitchio.utils.setup_logging(level=logging.INFO)
else:
    from loguru import logger as log

    from bot.logger import InterceptHandler

    twitchio.utils.setup_logging(handler=InterceptHandler(), level=logging.INFO)

__title__ = "Gorenmu-bot"
__author__ = "MrChuw"
__license__ = ""
__copyright__ = ""
__version__ = Configs.version

if __name__ == "__main__":
    log.info("Ligando bot", exc_info=True)

    async def main() -> None:
        adapter: StarletteAdapter = StarletteAdapter(host="localhost", domain=Configs.ApisConfig.join_url.human_repr())
        bot: Gorenmu = Gorenmu(configs=Configs, case_insensitive=True, log=log, adapter=adapter)
        # bot.site = api
        # bot.api_start = api_start
        await bot.DatabaseHandler.setup_database()
        await bot.LifecycleHandler.setup_internal()
        await bot.LifecycleHandler.setup()
        await bot.start()

    try:
        with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
            runner.run(main())
    except KeyboardInterrupt:
        log.warning("Shutting down due to KeyboardInterrupt...")
