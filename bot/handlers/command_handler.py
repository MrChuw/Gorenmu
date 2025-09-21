# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import pathlib
import traceback
import types
from importlib import import_module
from typing import TYPE_CHECKING

from loguru import logger
from twitchio.ext.commands import CommandErrorPayload

from bot.exceptions import CommandNotFound, CommandOnCooldown, DevRequired, GuardFailure, InvalidArgument, OwnerRequired
from bot.ext import Routine

if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.cogs.bug.command.bug import BugCmd
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
                if not hasattr(module, "setup"):
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
                    elif "routines" in folder.name:
                        self.load_routines(folder)
            self.start_routines()
        except Exception as e:
            logger.error(f"Failed to {'reload' if reload else 'load'} cogs: {e}", extra={"locals": locals()})

    async def load_cogs(self) -> None:
        await self._load_all_cogs(reload=False)

    async def reload_cogs(self) -> None:
        await self._load_all_cogs(reload=True)

    def is_enabled(self, ctx: Context, command: str = "") -> bool:
        return (command or ctx.command.name.lower()) not in self.bot.channels[ctx.channel.name].disabled

    @staticmethod
    def _get_module(path: pathlib.Path, filename: pathlib.Path) -> tuple[types.ModuleType, str]:
        local = os.path.join(path, filename.name)
        name = local[local.find("bot/cogs") : -3].replace("/", ".")
        package = ".".join(filename.parts[filename.parts.index("bot") :]).removesuffix(".py")
        module: types.ModuleType = import_module(name, package=package)
        return module, name

    async def send_bug(self, ctx: Context, error: Exception):
        command = self.bot.get_command("bug")
        url = self.bot.config.Discord.log_webhook
        component: BugCmd = command.component  # NOQA
        session = component.SessionsCaches.Bug.session
        discord_webhook = component.DiscordWebHook
        tb_str = "".join(traceback.format_exception(type(error), error, error.__traceback__))
        user_url = f"[@{ctx.author.name}](<https://twitch.tv/{ctx.author.name}>)"
        channel_url = f"[#{ctx.channel.name}](<https://twitch.tv/{ctx.channel.name}>)"
        await discord_webhook.send_discord_webhook(
            session,
            url,
            ctx,
            f"**Args used in the command:** **```{ctx.message.text}```**\n```py\n{tb_str}\n```",
            f"Error occurred while user {user_url} "
            f"was running the command: {ctx.command.name} "
            f"in {channel_url} channel.",
            f"https://twitch.tv/{ctx.author.name}",
            title2=f"Error occurred while user @{ctx.author.name} "
            f"was running the command: {ctx.command.name} "
            f"in #{ctx.channel.name} channel.",
        )

    async def event_command_error(self, payload: CommandErrorPayload) -> None:
        command = payload.context.command
        if command and command.has_error and payload.context.error_dispatched:
            return None

        ctx: Context = payload.context
        error: Exception = payload.exception
        if not self.bot.channels[ctx.channel.name].online:
            return None
        if ctx.prefix != self.bot.channels[ctx.channel.name].prefix:
            return None
        translations = ctx.command.component.translations

        if not isinstance(error, InvalidArgument):
            await self.send_bug(ctx, error)

        if isinstance(error, CommandNotFound):
            return None
        if isinstance(error, DevRequired):
            await ctx.simple_response(ctx, translations.Exceptions.dev_required(ctx).response_string)
            self.bot.log.warning(error)
        if isinstance(error, OwnerRequired):
            await ctx.simple_response(ctx, translations.Exceptions.owner_required(ctx).response_string)
        if isinstance(error, CommandOnCooldown):
            format_string = translations.SupportTools.TimeTools.Humanize.naturaltime(error.remaining, future=True)
            cooldown_str = translations.Exceptions.command_on_cooldown(ctx, format_string)
            return await ctx.simple_response(ctx, cooldown_str.response_string)
        if isinstance(error, NotImplementedError):
            return await ctx.simple_response(ctx, translations.Exceptions.not_implemented(ctx).response_string)
        if isinstance(error, InvalidArgument) and ctx.command:
            teste = ctx.command.component.translations.get_decorator(ctx=ctx)
            await ctx.reply(teste.deco_usage(ctx, prefix=ctx.prefix))
            return None
        if isinstance(error, GuardFailure):
            return None
        self.bot.log.error(error)
        return await ctx.simple_response(
            ctx, translations.Exceptions.error_not_registered(ctx, self.bot.dev_name).response_string
        )
