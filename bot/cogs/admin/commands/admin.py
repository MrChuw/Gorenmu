# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import sys
from typing import TYPE_CHECKING

from bot.ext import commands, Context
from bot.translations import BaseDecorators, Response, TranslationManager
from bot.utils import Role

if TYPE_CHECKING:
    from bot.bot import Gorenmu

BaseAdmin = BaseDecorators.Admin


class AdminSmallCmds(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None:
        ...

    @commands.Component.guard()
    def is_dev(self, ctx: commands.Context) -> bool:
        return Role.dev(ctx)

    @commands.base_decorator(BaseAdmin.Nada)
    @commands.command(name='nada', aliases=[])
    async def nada(self, ctx: Context, *, args, ) -> Response:
        translations = ctx.user.translations.Admin.Nada
        teste = ctx.bot.ToolsTools.remove_prefixed_option(args, "title:")
        return translations.nada.format_response(ctx, args, success=True, handle=None, response_list=[])

    @commands.base_decorator(BaseAdmin.Restart)
    @commands.command(name="restart", aliases=[])
    async def restart(self, ctx: Context) -> Response:
        translations = ctx.user.translations.Admin.Restart
        if venv_python := os.getenv("VIRTUAL_ENV"):
            python_executable = os.path.join(venv_python, "bin", "python")
        else:
            python_executable = sys.executable
        try:
            os.execv(python_executable, [python_executable] + sys.argv)
        except Exception as e:
            self.bot.log.error(e)
            return translations.unexpected_error.format_response(ctx, e, success=False)

    @commands.base_decorator(BaseAdmin.Reload)
    @commands.command(name='reload', aliases=[], invoke_fallback=True)
    async def reload(self, ctx: Context, command: str) -> Response:
        translations = ctx.user.translations.Admin.Reload
        if command == "translations":
            try:
                ctx.bot.TranslationManager = TranslationManager()
                return translations.translations_reloaded.format_response(ctx)
            except Exception as e:
                self.bot.log.error(e)
                return translations.translations_reloaded_error.format_response(ctx, e, success=False)
        if command == "all":
            await ctx.bot.CommandHandler.reload_cogs(ctx.bot)
            return translations.commands_reloaded.format_response(ctx)
        command_to_reload = ctx.bot.get_command(command)
        if not command_to_reload:
            return translations.command_not_found.format_response(ctx, command, success=False)
        module = command_to_reload.module
        try:
            await self.bot.reload_module(module)
            return translations.command_reloaded.format_response(ctx, command)
        except Exception as e:
            self.bot.log.error(e)
            return translations.command_reloaded_error.format_response(ctx, command, e, success=False)

    @commands.base_decorator(BaseAdmin.DisableNSFW)
    @commands.command(name='disable_nsfw', aliases=[])
    async def disable_nsfw(self, ctx: Context, *, args, ) -> Response:  # TODO: To Make.
        translations = ctx.user.translations.Admin.DisableNSFW
        try:
            for channel in self.bot.channels:
                self.bot.channels[channel].disabled.update(self.bot.CommandHandler.COMMANDS_TO_DISABLE)
                await self.bot.channels[channel].save()
            return translations.success.format_response(ctx, args, success=True)
        except Exception as e:
            self.bot.log.error(e)
            return translations.unexpected_error.format_response(ctx, e, success=False)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(AdminSmallCmds(bot))


async def teardown(bot: Gorenmu) -> None:
    ...
