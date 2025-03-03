# -*- coding: utf-8 -*-
import os
from loguru import logger

from bot.bot import Gorenmu
from bot.ext.config import Config
from bot.api import api, api_start

config_yml = os.path.join(os.path.dirname(__file__), "config.toml")

Configs = Config(config_yml)

__title__ = "Gorenmu-bot"
__author__ = "MrChuw"
__license__ = ""
__copyright__ = ""
__version__ = Configs.version

if __name__ == "__main__":
    logger.info("Ligando bot", exc_info=True)
    quantidade = 0

    while True:
        quantidade += 1
        logger.info(quantidade)
        try:
            bot = Gorenmu(configs=Configs, case_insensitive=True, retain_cache=True, log=logger)
            bot.site = api
            bot.api_start = api_start
            bot.start()
            bot.loop.run_forever()
        except KeyboardInterrupt:
            # bot.loop.run_until_complete(bot.stop())
            # bot.loop.close()
            break
        except BaseException as e:
            logger.exception(e, extra={"locals": locals()})
            logger.info(f"{quantidade}: BaseException")  # finally:  #     bot.loop.run_until_complete(bot.stop())
