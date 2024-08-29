# -*- coding: utf-8 -*-
import os

from bot.bot import Gorenmu
from bot.ext.config import Config

# from bot.logger import log
from loguru import logger

config_yml = os.path.join(os.path.dirname(__file__), "config.toml")

Configs = Config(config_yml)

__title__ = "Gorenmu-bot"
__author__ = "MrChuw"
__license__ = ""
__copyright__ = ""
__version__ = Configs.version

log = logger

if __name__ == "__main__":
    log.info("Ligando bot", exc_info=True)
    quantidade = 0

    while True:
        quantidade += 1
        log.info(quantidade)
        try:
            bot = Gorenmu(configs=Configs, case_insensitive=True, retain_cache=True, log=log)
            bot.start()
            bot.loop.run_forever()
        except KeyboardInterrupt:
            # bot.loop.run_until_complete(bot.stop())
            # bot.loop.close()
            break
        except BaseException as e:
            log.exception(e, extra={"locals": locals()})
            log.info(f"{quantidade}: BaseException")  # finally:  #     bot.loop.run_until_complete(bot.stop())
