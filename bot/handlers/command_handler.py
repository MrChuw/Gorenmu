# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import pathlib
import types
from importlib import import_module
from typing import Any, TYPE_CHECKING

from loguru import logger
from twitchio.ext.commands import Command, CommandErrorPayload

from bot.exceptions import CommandNotFound, CommandOnCooldown, DevRequired, GuardFailure, InvalidArgument, OwnerRequired
from bot.ext import Routine

if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.ext import Context


class CommandHandler:
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot

    def start_routines(self) -> None:
        for routine in self.bot.routines:
            routine.start(self.bot)

    def stop_routines(self) -> None:
        try:
            for routine in self.bot.routines:
                routine.cancel()
        except Exception as e:
            logger.error(e)

    async def load_command_module(self, path: pathlib.Path) -> None:
        for filename in path.iterdir():
            if filename.suffix != ".py" or filename.name.startswith("__"):
                continue

            try:
                module, name = self._get_module(path=path, filename=filename)
                if not getattr(module, "setup"):
                    continue
                command_name = [
                    modulo for modulo in module.__dict__ if modulo.endswith("Cmd") or modulo.endswith("Cmds")
                ][0]
                if not self.bot.get_component(command_name):
                    await self.bot.load_module(name)
                else:
                    await self.bot.reload_module(name)
            except Exception as e:
                self.bot.log.error(
                    f"Command '{filename.name[:-3]}' failed to load: {e} in {filename.joinpath()}",
                    extra={"locals": locals()},
                )

    def load_manual_event_message(self, path: pathlib.Path) -> None:
        for filename in path.iterdir():
            if filename.suffix != ".py" or filename.name.startswith("__"):
                continue
            try:
                module, name = self._get_module(path=path, filename=filename)
                if hasattr(module, "event_message"):
                    self.bot.manual_event_message.append(module.event_message)
            except Exception as e:
                logger.error(f"Listener '{filename[:-3]}' failed to load: {e}", extra={"locals": locals()})

    def load_routines(self, path: pathlib.Path) -> None:
        for filename in path.iterdir():
            if filename.suffix != ".py" or filename.name.startswith("__"):
                continue
            try:
                module, name = self._get_module(path=path, filename=filename)
                routine: Routine = module.routine
                self.bot.routines.append(routine)
            except Exception as e:
                logger.error(f"Routine '{filename.name[:-3]}' failed to load: {e}", extra={"locals": locals()})

    async def _load_all_cogs(self, *, reload: bool = False) -> None:
        if reload:
            self.stop_routines()

        cogs = pathlib.Path(__file__).parent.parent / "cogs"
        try:
            for cog in cogs.iterdir():
                if cog.is_file() or ".example" in cog.name:
                    continue
                for folder in cog.iterdir():
                    if folder.name in {"__pycache__", "data"}:
                        continue
                    if "commands" in folder.name or "command" in folder.name:
                        await self.load_command_module(folder)
                    elif "manual_event_message" in folder.name:
                        self.load_manual_event_message(folder)
                    elif "routines" in folder.name:
                        self.load_routines(folder)
            self.start_routines()
        except Exception as e:
            logger.error(f"Failed to {'reload' if reload else 'load'} cogs: {e}", extra={"locals": locals()})

    async def load_cogs(self) -> None:
        await self._load_all_cogs(reload=False)

    async def reload_cogs(self) -> None:
        await self._load_all_cogs(reload=True)

    @staticmethod
    def load_language(ctx: Context):
        channel = ctx.channel.name
        channel = ctx.bot.channels[channel]
        ctx.translations = ctx.bot.TranslationManager.get_translations(ctx.user.language or channel.language or "en")

    def is_enabled(self, ctx: Context, command: str = "") -> bool:
        return (command or ctx.command.name.lower()) not in self.bot.channels[ctx.channel.name].disabled

    @staticmethod
    def _get_module(path: pathlib.Path, filename: pathlib.Path) -> tuple[types.ModuleType, str]:
        local = os.path.join(path, filename.name)
        name = local[local.find("bot/cogs") : -3].replace("/", ".")
        package = ".".join(filename.parts[filename.parts.index("bot") :]).removesuffix(".py")
        module: types.ModuleType = import_module(name, package=package)
        return module, name

    async def event_command_error(self, payload: CommandErrorPayload) -> None:
        command: Command[Any, ...] | None = payload.context.command
        if command and command.has_error and payload.context.error_dispatched:
            return None

        ctx: Context = payload.context
        error: Exception = payload.exception
        if not self.bot.channels[ctx.channel.name].online:
            return None
        if ctx.prefix != self.bot.channels[ctx.channel.name].prefix:
            return None
        translations = ctx.user.translations.Exceptions
        if isinstance(error, CommandNotFound):
            return None
        if isinstance(error, DevRequired):
            await ctx.simple_response(ctx, translations.dev_required)
            self.bot.log.warning(error)
        if isinstance(error, OwnerRequired):
            await ctx.simple_response(ctx, translations.owner_required)
        if isinstance(error, CommandOnCooldown):
            format_string = ctx.user.translations.SupportTools.TimeTools.Humanize.naturaltime(
                error.remaining, future=True
            )
            cooldown_str = translations.command_on_cooldown.format(format_string)
            return await ctx.simple_response(ctx, cooldown_str)
        if isinstance(error, NotImplementedError):
            return await ctx.simple_response(ctx, translations.not_implemented)
        if isinstance(error, InvalidArgument) and ctx.command:
            decorator = ctx.bot.TranslationManager.get_decorator(ctx.command, ctx)
            await ctx.reply(decorator.usage.format(ctx.prefix))
            return None
        if isinstance(error, GuardFailure):
            return None
        self.bot.log.error(error)
        return await ctx.simple_response(ctx, translations.error_not_registered.format(self.bot.dev_name))
