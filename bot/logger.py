import logging

from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except KeyError:
            level = record.levelno
        frame = logging.currentframe()
        while frame and frame.f_code.co_filename in logging._srcfile:
            frame = frame.f_back

        logger.opt(depth=6, exception=record.exc_info).log(level, record.getMessage())
