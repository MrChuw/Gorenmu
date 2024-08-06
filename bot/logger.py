# -*- coding: utf-8 -*-
import logging
import sys

from loguru import logger

from bot.ext.config import LoggerConfig


def log(Configs: LoggerConfig) -> logger:
    logger.remove()
    format = Configs.format
    level = Configs.level
    enqueue = Configs.enqueue
    colorize = Configs.colorize

    logger.add(sys.stderr, format=format, level=level, enqueue=enqueue, colorize=colorize)
    return logger

class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Obter o nível correspondente ao Loguru
        try:
            level = logger.level(record.levelname).name
        except KeyError:
            level = record.levelno

        # Captura a stack frame correta
        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        # Registra a mensagem de log no Loguru.
        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

# Configurar o logger padrão do Python para usar o InterceptHandler
logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)