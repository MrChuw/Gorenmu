from __future__ import annotations

from contextlib import asynccontextmanager
import loguru
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from logging import getLogger, StreamHandler
from bot_site.utils import BotAPIRequestCache
import time
from fastapi.middleware.gzip import GZipMiddleware
import minify_html


log = loguru.logger
request_cache = BotAPIRequestCache()


@asynccontextmanager
async def lifespan(app: FastAPI):
    class LoguruHandler(StreamHandler):
        def emit(self, record):
            loguru_log = self.format(record)
            log.info(loguru_log)

    loguru_handler = LoguruHandler()

    for log_name in ["uvicorn", "uvicorn.access", "fastapi"]:
        logger_to_replace = getLogger(log_name)
        logger_to_replace.handlers = []
        logger_to_replace.addHandler(loguru_handler)
        logger_to_replace.setLevel("INFO")

    yield
    await request_cache.session.close()


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="bot_site/static"), name="static")
app.mount("/images", StaticFiles(directory="bot_site/images"), name="images")
app.add_middleware(SessionMiddleware, secret_key="your-secret-key", max_age=3600)  # NOQA
app.add_middleware(GZipMiddleware, minimum_size=500, compresslevel=5)  # NOQA

templates = Jinja2Templates(directory="bot_site/templates")
default_headers = {"Access-Control-Expose-Headers": "*"}


@app.middleware("http")
async def add_default_headers(request, call_next):
    # Isso acontece primeiro do que a função da rota chamada
    start_time = time.perf_counter()
    response: Response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


async def template_handler(template: str, extra_context: dict):
    template = templates.TemplateResponse(template, extra_context)
    content = template.body.decode("utf-8")
    template.body = minify_html.minify(content,
                                       minify_js=True,
                                       minify_css=True,
                                       remove_processing_instructions=True,
                                       keep_ssi_comments=True
                                       ).encode("utf-8")
    template.headers.update({"Content-Length": str(len(template.body))})
    return template



@app.get("/")
@app.get("/{lang}/")
async def index(request: Request):
    return await template_handler("index.html", {"request": request})


# Home page
@app.get("/home")
@app.get("/{lang}/home")
async def home(request: Request, lang: str = 'en'):
    request_params = request.query_params
    if "partial" in request_params and request_params["partial"] == "true":
        return await template_handler("partials/home.html", {"request": request})
    return await template_handler("index.html", {"request": request})


# Changelog
@app.get("/changelog")
@app.get("/{lang}/changelog")
async def changelog(request: Request, lang: str = 'en'):
    request_params = request.query_params
    if "partial" in request_params and request_params["partial"] == "true":
        return await template_handler("partials/changelog.html", {"request": request})
    return await template_handler("changelog.html", {"request": request})


# Images
@app.get("/image/{path:path}")
async def get_image(request: Request, path: str):
    request_params = request.query_params
    if "partial" in request_params and request_params["partial"] == "true":
        return HTMLResponse(content=f'<img src="/images/{path}">')
    return FileResponse(f"images/{path}")


@app.get("/changeLangs")
async def changelang(request: Request):
    request.session["lang"] = request.query_params.get("lang")
    return RedirectResponse(url=request.headers.get("Referer"), status_code=302)




# if __name__ == "__main__":
    # import uvicorn
    # uvicorn.run("router:app", host="0.0.0.0", port=8900, log_level="info", reload=True, reload_dirs=["site"])
    # uvicorn.run("router:app", host="0.0.0.0", port=5000, log_level="info")
