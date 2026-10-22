from __future__ import annotations

import os
import pathlib
import traceback
import types
from importlib import import_module
from typing import TYPE_CHECKING, Any

from loguru import logger
from twitchio.ext.commands import CommandErrorPayload

from bot.exceptions import (
    CommandDisabledError,
    CommandNotFound,
    CommandOnCooldown,
    DevRequiredError,
    GuardFailure,
    InvalidArgument,
    OwnerRequiredError,
)
from bot.ext import Routine
from bot.ext.translations.translations import LangDict, TBase, TranslationBase

from bot.ext import Context

if TYPE_CHECKING:
    from twitchio import ChatMessage

    from bot.bot import Gorenmu
    from bot.cogs.bug.command.bug import BugCmd



class CommandHandler:
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.lang_dict: LangDict = LangDict(bot)

    @staticmethod
    def _get_module(path: pathlib.Path, filename: pathlib.Path) -> tuple[types.ModuleType, str]:
        local = os.path.join(path, filename.name)
        name = local[local.find("bot/cogs") : -3].replace("/", ".")
        package = ".".join(filename.parts[filename.parts.index("bot") :]).removesuffix(".py")
        module: types.ModuleType = import_module(name, package=package)
        return module, name

    async def teardown_all_commands(self) -> None:
        modules = list(self.bot.modules.keys())
        for command_name in modules:
            await self.bot.unload_module(command_name)
            ...
        ...

    async def load_command_module(self, path: pathlib.Path) -> None:
        for filename in path.iterdir():
            if filename.suffix != ".py" or filename.name.startswith("__"):
                continue

            try:
                module, name = self._get_module(path=path, filename=filename)
                if not hasattr(module, "setup"):
                    continue
                command_name = next(
                    modulo for modulo in module.__dict__ if modulo.endswith("Cmd") or modulo.endswith("Cmds")
                )
                if not self.bot.get_component(command_name):
                    await self.bot.load_module(name)
                else:
                    await self.bot.reload_module(name)
            except Exception as e:
                self.bot.log.error(
                    f"Command '{filename.name[:-3]}' failed to load: {e} in {filename.joinpath()}",
                    extra={"locals": locals()},
                )

    async def load_routines(self, path: pathlib.Path) -> None:
        for filename in path.iterdir():
            if filename.suffix != ".py" or filename.name.startswith("__"):
                continue
            try:
                module, _ = self._get_module(path=path, filename=filename)
                routine: Routine = module.routine
                # TODO: To test.
                await self.bot.RoutineHandler.add_routine(str(path), routine)
            except Exception as e:
                logger.error(f"Routine '{filename.name[:-3]}' failed to load: {e}", extra={"locals": locals()})

    async def _load_all_cogs(self, *, reload: bool = False) -> None:
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
                    elif "routines" in folder.name or "routine" in folder.name:
                        await self.load_routines(folder)
        except Exception as e:
            logger.error(f"Failed to {'reload' if reload else 'load'} cogs: {e}", extra={"locals": locals()})

    async def load_cogs(self) -> None:
        await self._load_all_cogs(reload=False)

    async def reload_cogs(self) -> None:
        await self._load_all_cogs(reload=True)

    async def is_enabled(self, target: Context | ChatMessage, command: str = "") -> bool:
        channel_commands = self.bot.channels.disabled(target)
        command_inner = ""
        if isinstance(target, Context):
            if target.command:
                command_inner: str = target.command.name.lower()
        else:
            ctx = await self.bot.LifecycleHandler.get_context(target)
            command_inner  = ctx.command.name.lower()
        command = command or command_inner

        return command not in channel_commands

    # def is_enabled(self, ctx: Context, command: str = "") -> bool:
    #     return (command or ctx.command.name.lower()) not in self.bot.channels[ctx.channel.name].disabled


    async def send_bug(self, ctx: Context, error: Exception, ping: bool = True):
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
            ping=ping,
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
        translations: TranslationBase = ctx.command.component.translations
        translations.ctx_set(ctx)
        if not isinstance(error, (InvalidArgument, CommandOnCooldown, CommandDisabledError, CommandNotFound)):
            await self.send_bug(ctx, error)

        if isinstance(error, (CommandNotFound, CommandDisabledError)):
            return None
        if isinstance(error, DevRequiredError):
            await ctx.simple_response(ctx, translations.Exceptions.dev_required(ctx).response_string)
            self.bot.log.warning(error)
        if isinstance(error, OwnerRequiredError):
            await ctx.simple_response(ctx, translations.Exceptions.owner_required(ctx).response_string)
        if isinstance(error, CommandOnCooldown):
            format_string = translations.SupportTools.TimeTools.Humanize(ctx.user.get_lang()).naturaltime(
                error.remaining, future=True
            )
            cooldown_str = translations.Exceptions.command_on_cooldown(format_string)
            return await ctx.simple_response(ctx, cooldown_str.response_string)
        if isinstance(error, NotImplementedError):
            return await ctx.simple_response(ctx, translations.Exceptions.not_implemented(ctx).response_string)
        if isinstance(error, InvalidArgument) and ctx.command:
            deco = translations.get_decorator(ctx=ctx)
            if not deco:
                return None  # TODO: Message of usage not implemented, pls contact dev.
            await ctx.reply(deco.deco_usage(ctx=ctx, prefix=ctx.prefix))
            return None
        if isinstance(error, GuardFailure):
            return None
        self.bot.log.error(error)
        return await ctx.simple_response(
            ctx, translations.Exceptions.error_not_registered(self.bot.dev_user.display_name).response_string
        )

    async def wait_for(self, event: str, *, timeout: float | None = None, predicate=None, **kwargs) -> Any:
        if predicate and kwargs:
            original_predicate = predicate

            async def injected_predicate(payload):
                return await original_predicate(payload, **kwargs)

            predicate = injected_predicate

        return await self.bot.wait_for(event, timeout=timeout, predicate=predicate)

    async def wait_for_message(self, *, timeout: float | None = None, predicate=None, **kwargs) -> ChatMessage:
        if predicate and kwargs:
            original_predicate = predicate

            async def injected_predicate(payload):
                return await original_predicate(payload, **kwargs)

            predicate = injected_predicate

        return await self.bot.wait_for("message", timeout=timeout, predicate=predicate)

    async def generic_wait(self, payload: ChatMessage, ctx: Context, target_name: str, generic_wait) -> bool:
        # return True
        if payload.chatter.id == self.bot.bot_id or payload.source_broadcaster is not None:
            return False
        if (payload.chatter.name or "").lower() != target_name:
            return False
        if (payload.broadcaster.name or "").lower() != (ctx.broadcaster.name or "").lower():
            return False
        return payload.text.lower() in generic_wait.accept() + generic_wait.reject()

    async def setup(self): ...

    async def teardown(self) -> None: ...
