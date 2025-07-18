# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import sys
from typing import TYPE_CHECKING

from bot.ext import commands, Context
from bot.translations import Response, Translations
from bot.utils import Role

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    translations_t = Translations.Admin.Reload


class AdminSmallCmds(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot

    name = "Admin Commands"
    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def is_dev(self, ctx: Context) -> bool:
        return Role.dev(ctx)

    @commands.base_decorator("Admin.Nada")
    @commands.command(name="nada", aliases=[])
    async def nada(self, ctx: Context, *, args) -> Response:
        translations = ctx.user.translations.Admin.Nada
        # for command_name in self.bot.commands:
        #     command = self.bot.commands[command_name]
        #     if hasattr(command, "commands"):
        #         for subcommand_name in command.commands:
        #             try:
        #                 subcommand = command.commands[subcommand_name]
        #                 decorator = ctx.bot.TranslationManager.get_decorator(subcommand, ctx)
        #                 print(decorator.usage)
        #             except Exception as e:
        #                 print(e)
        #     decorator = ctx.bot.TranslationManager.get_decorator(command, ctx)
        #     print(decorator.usage)
        "mr_c​huw"
        args = "asdfasdf mr_️chuw VARIATION SELECTOR-16"
        await ctx.send(args)
        return translations.nada.format_response(ctx, args, success=True, handle=None, response_list=[])

    @commands.base_decorator("Admin.Restart")
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

    @commands.base_decorator("Admin.Reload")
    @commands.command(name="reload", aliases=[])
    async def reload(self, ctx: Context, command: str) -> Response:
        translations = ctx.user.translations.Admin.Reload

        reloader_map = {
            "translations": {
                "attr": "TranslationManager",
                "module": "bot.translations",
                "class": "TranslationManager",
                "args": [],
            },
            "emotes": {"attr": "Emotes", "module": "bot.apis.emotes", "class": "Emotes", "args": [self.bot]},
            "tokens_handler": {
                "attr": "TokensHandler",
                "module": "bot.handlers.tokens_handler",
                "class": "TokensHandler",
                "args": [self.bot],
            },
            "channel_handler": {
                "attr": "ChannelHandler",
                "module": "bot.handlers.channel_handler",
                "class": "ChannelHandler",
                "args": [self.bot],
            },
            "lifecycle_handler": {
                "attr": "LifecycleHandler",
                "module": "bot.handlers.lifecycle_handler",
                "class": "LifecycleHandler",
                "args": [self.bot],
            },
            "command_handler": {
                "attr": "CommandHandler",
                "module": "bot.handlers.command_handler",
                "class": "CommandHandler",
                "args": [self.bot],
            },
            "session_caches": {
                "attr": "SessionsCaches",
                "module": "bot.utils.cache_sessions",
                "class": "SessionsCaches",
                "args": [self.bot],
            },
            "string_mani": {
                "attr": "StringTools",
                "module": "bot.utils.string_manipulation",
                "class": "StringTools",
                "args": [],
            },
        }

        if command == "commands":
            await ctx.bot.CommandHandler.reload_cogs()
            return translations.commands_reloaded.format_response(ctx)

        if command == "all":
            results = []
            for key in ["commands", *reloader_map]:
                fake_ctx = await self.reload._callback(self, ctx, command=key)  # NOQA
                results.append(fake_ctx.response_string)
            return translations.all.format_response(ctx, " ".join(results))

        if command in reloader_map:
            config = reloader_map[command]
            try:
                await ctx.bot.reload_component(
                    attr_name=config["attr"],
                    module_name=config["module"],
                    class_name=config["class"],
                    args=config.get("args", []),
                )
                return translations.module_reloaded.format_response(ctx, config["attr"])
            except Exception as e:
                ctx.bot.log.error(e)
                return translations.module_reloaded_error.format_response(ctx, config["attr"], e, success=False)

        command_to_reload = ctx.bot.get_command(command)
        if not command_to_reload:
            return translations.command_not_found.format_response(ctx, command, success=False)

        module = command_to_reload.module
        try:
            await ctx.bot.reload_module(module)
            return translations.command_reloaded.format_response(ctx, command)
        except Exception as e:
            ctx.bot.log.error(e)
            return translations.command_reloaded_error.format_response(ctx, command, e, success=False)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(AdminSmallCmds(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
