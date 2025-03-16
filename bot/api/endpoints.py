## Here will only be the endpoints of things for the site to use.
from __future__ import annotations
from typing import TYPE_CHECKING
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from logging import getLogger, StreamHandler

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class FastAPIWithBot(FastAPI):
    bot: Gorenmu



app = FastAPIWithBot()



@app.get("/api")
async def index(request: Request):
    teste = app.bot.TranslationManager.languages["en"].strings
    return {"data": teste}


@app.get("/api/languages")
async def get_languages(request: Request):
    return {"data": app.bot.TranslationManager.languages.keys()}


@app.get("/api/translation/{language}")
async def get_translation(request: Request, language: str):
    return {"data": app.bot.TranslationManager.get_translation(language, request.query_params.get("key"))}





async def start(bot: Gorenmu):
    app.bot = bot  # NOQA

    class LoguruHandler(StreamHandler):
        def emit(self, record):
            loguru_log = self.format(record)
            app.bot.log.info(loguru_log)

    loguru_handler = LoguruHandler()

    config = uvicorn.Config(app, host="0.0.0.0", port=3308, log_level="info")

    server = uvicorn.Server(config=config)

    for log_name in ["uvicorn", "uvicorn.access", "fastapi"]:
        logger_to_replace = getLogger(log_name)
        logger_to_replace.handlers = []
        logger_to_replace.addHandler(loguru_handler)
        logger_to_replace.setLevel("INFO")

    await server.serve()




# if __name__ == "__main__":


    # uvicorn.run("bot.site.teste:app", host="0.0.0.0", port=8900, log_level="info", reload=True)
    # uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info", reload=True)
