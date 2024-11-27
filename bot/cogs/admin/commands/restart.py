# -*- coding: utf-8 -*-
import os
import sys

from bot.bot import Gorenmu
from bot.ext.commands import base_decorator, Bucket, check, command, Command, Context, cooldown
from bot.translations import BaseDecorators, Response
from bot.utils import Role


@base_decorator(BaseDecorators.Admin.Restart)
@cooldown(rate=3, per=10, bucket=Bucket.user)
@check([Role.dev])
@command(name="restart", aliases=[])
async def command(ctx: Context) -> Response:
    translations = ctx.translations.Admin.Restart
    if venv_python := os.getenv("VIRTUAL_ENV"):
        python_executable = os.path.join(venv_python, "bin", "python")
    else:
        python_executable = sys.executable
    try:
        os.execv(python_executable, [python_executable] + sys.argv)
    except Exception as e:
        return translations.unexpected_error.format_response(ctx, e, success=False)
