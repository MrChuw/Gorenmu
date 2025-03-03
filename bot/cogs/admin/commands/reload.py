# -*- coding: utf-8 -*-
from bot.bot import Gorenmu
from bot.ext.commands import base_decorator, Bucket, check, command, Command, Context, cooldown
from bot.translations import BaseDecorators, Response
from bot.utils import Role
import importlib
import sys



@base_decorator(BaseDecorators.Admin.Reload)
@cooldown(rate=3, per=10, bucket=Bucket.user)
@check([Role.dev])
@command(name='reload', aliases=[])
async def command(ctx: Context, module: str = "") -> Response:
    if module:
        reload_module_and_dependencies(module)
    ctx.bot.CommandHandler.reload_cogs(ctx.bot)
    return ctx.translations.Admin.Reload.commands_reloaded.format_response(ctx)


def reload_module_and_dependencies(module_name):
    for mod_name in list(sys.modules):
        if mod_name.startswith("bot."):
            ...
        if mod_name.startswith(module_name):
            importlib.reload(sys.modules[mod_name])


