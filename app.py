# -*- coding: utf-8 -*-
from aiohttp.web import Application, Response, RouteTableDef, run_app

import somali
from somali import config

routes = RouteTableDef()


@routes.get("/")
async def root(request):
    return Response(text=f"{somali.__title__} v{somali.__version__}")


if __name__ == "__main__":
    app = Application()
    app.add_routes(routes)
    run_app(app, host=config.host, port=config.port)
