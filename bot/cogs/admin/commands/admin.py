from __future__ import annotations

import asyncio
import importlib.util
import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from bot.ext import Context, Response, commands
from bot.utils import Role, SessionsCaches, StringTools
from bot.utils.singleton import Singleton

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class AdminSmallCmds(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot)
        self.SessionsCaches: SessionsCaches = SessionsCaches(bot)
        self.StringTools: StringTools = StringTools()

    name = "Admin Commands"
    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def is_dev(self, ctx: Context) -> bool:
        return Role.dev(ctx)

    @commands.command(name="nada", aliases=["bonjour", "hello"])
    async def nada(self, ctx: Context, *, args: str) -> Response:
        # if " " in args:
        #     command, subcommand = args.split()
        #     command = ctx.bot.get_command(command)
        #     try:
        #         command = command.get_command(subcommand)
        #     except Exception as e:
        #         print(e)
        #
        #     teste = command.component.translations.get_decorator(ctx=command)
        #     teste2 = teste.deco_usage(ctx, prefix=ctx.prefix)
        #     await ctx.reply(teste2)
        return self.translations.Nada.nada(ctx, args + self.StringTools.inv_char())
        # return self.translations.Exceptions.empty(ctx, args)

    @commands.command(name="restart", aliases=[])
    async def restart(self, ctx: Context) -> Response:
        if venv_python := os.getenv("VIRTUAL_ENV"):
            python_executable = os.path.join(venv_python, "bin", "python")
        else:
            python_executable = sys.executable
        try:
            os.execv(python_executable, [python_executable, *sys.argv])
        except Exception as e:
            self.bot.log.error(e)
            return self.translations.Restart.unexpected_error(ctx, e)

    @commands.command(name="reload", aliases=[])
    async def reload(self, ctx: Context, command: str, *, extras=False) -> Response:
        translations = self.translations.Reload

        reloader_map = {
            # "emotes": {"attr": "Emotes", "module": "bot.apis.emotes", "class": "Emotes", "args":
            # [self.bot, self.SessionsCaches.EmotesCachedSession.session]},
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
        }

        if command == "commands":
            await ctx.bot.CommandHandler.reload_cogs()
            return translations.commands_reloaded(ctx)

        if command == "all":
            Singleton.clear()
            results = []
            for key in ["translations", "commands", *reloader_map]:
                fake_ctx = await self.reload._callback(self, ctx, command=key)  # NOQA
                results.append(fake_ctx.response_string)
            return self.translations.Exceptions.echo(ctx, " ".join(results))

        if command in reloader_map:
            config = reloader_map[command]
            try:
                await reload_component(
                    self.bot,
                    attr_name=config["attr"],
                    module_name=config["module"],
                    class_name=config["class"],
                    args=config.get("args", []),
                )
                return translations.module_reloaded(ctx, config["attr"])
            except Exception as e:
                ctx.bot.log.error(e)
                return translations.module_reloaded_error(ctx, config["attr"], e)

        if command == "translations":
            from bot.utils.reload_util import (
                reload_all_translations,
                reload_and_get_authorized,
            )

            force = bool(extras)
            try:
                new_base = await reload_and_get_authorized("bot.ext.translations", "TranslationBase", force)
                new_cls = await reload_all_translations("Translations", force)
                for cls in new_cls:
                    cls.__bases__ = (new_base,)
                await ctx.bot.CommandHandler.reload_cogs()
                return translations.module_reloaded(ctx, "Translations")
            except Exception as e:
                ctx.bot.log.error(e)
                return translations.module_reloaded_error(ctx, "Translations", e)

        command_to_reload = ctx.bot.get_command(command)
        if not command_to_reload:
            return translations.command_not_found(ctx, command)

        try:
            spec = importlib.util.find_spec(command_to_reload.module)
            await ctx.bot.CommandHandler.load_command_module(Path(spec.origin).parent)
            return translations.command_reloaded(ctx, command)
        except Exception as e:
            ctx.bot.log.error(e)
            return translations.command_reloaded_error(ctx, command, e)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(AdminSmallCmds(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA


async def reload_component(bot_obj, attr_name: str, module_name: str, class_name: str, args: list | None = None):
    from bot.utils.reload_util import reload_and_get_authorized

    try:
        new_class = await reload_and_get_authorized(module_name, class_name)
        instance = new_class(*args) if args else new_class()
        old_instance = getattr(bot_obj, attr_name)
        if close_attr := getattr(old_instance, "close", None):
            if asyncio.iscoroutinefunction(close_attr):
                if old_instance.__class__.__name__ != "LifecycleHandler":
                    await close_attr()
            else:
                close_attr()
        setattr(bot_obj, attr_name, instance)
        bot_obj.log.info(f"Reloaded {attr_name} from {module_name}.{class_name}")
    except Exception as e:
        bot_obj.log.error(f"Error reloading {attr_name}: {e}")
        raise
