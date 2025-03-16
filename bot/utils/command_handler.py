# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import pathlib
import types
from importlib import import_module
from typing import TYPE_CHECKING

from loguru import logger
from twitchio.ext.commands import BucketType
from bot.ext import Routine

if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.ext import Context


class CommandHandler:
    def __init__(self) -> None:
        pass

    # TODO: Uma forma de desabilitar os subcomandos do booru.

    COMMANDS_TO_DISABLE = {"booru": 411010313, "gelbooru": 411010313, "danbooru": 411010313, "rule34": 411010313,
                           "realbooru": 411010313, "tbib": 411010313, "xbooru": 411010313, "safebooru": 411010313,
                           "yandere": 411010313, "lolibooru": 411010313, "kanachan": 411010313,
                           "kanachan_net": 411010313, "hypnohub": 411010313, "e621": 411010313, "e926": 411010313,
                           "derpibooru": 411010313, "furbooru": 411010313, "atfbooru": 411010313, "behoimi": 411010313,
                           "paheal": 411010313,
                           }

    DEFAULT_COOLDOWN_PER = 5
    DEFAULT_COOLDOWN_RATE = 2
    DEFAULT_COOLDOWN_BUCKET = BucketType.user

    @staticmethod
    def start_routines(self: Gorenmu) -> None:
        for routine in self.routines:
            routine.start(self)

    @staticmethod
    def stop_routines(self: Gorenmu) -> None:
        try:
            for routine in self.routines:
                routine.cancel()
        except Exception as e:
            logger.error(e)

    @staticmethod
    async def load_commands(bot: Gorenmu, path: pathlib.Path) -> None:
        for filename in path.iterdir():
            if not filename.suffix == ".py" or filename.name.startswith("__"):
                continue
            try:
                # if filename.name in ['imgur.py', 'imgur_repeated.py', 'nada.py', 'reload.py']:
                if filename.name in ['cookies.py']:
                    pass
                local: str = os.path.join(path, filename.name)
                name: str = local[:-3].replace("/", ".")
                package: str = ".".join(filename.parts)
                module: types.ModuleType = import_module(name, package=package)
                if not getattr(module, "setup"):
                    continue
                command_name = [modulo for modulo in module.__dict__ if modulo.endswith('Cmd') or modulo.endswith('Cmds')][0]
                if not bot.get_component(command_name):
                    await bot.load_module(name)
                else:
                    await bot.reload_module(name)


            except Exception as e:
                logger.error(f"Command '{filename.name[:-3]}' failed to load: {e} in {filename.joinpath()}",
                             extra={"locals": locals()}, )

    @staticmethod
    def load_manual_event_message(bot: Gorenmu, path: pathlib.Path) -> None:
        for filename in path.iterdir():
            if not filename.suffix == ".py" or filename.name.startswith("__"):
                continue
            try:
                local: str = os.path.join(path, filename.name)
                name: str = local[:-3].replace("/", ".")
                package: str = ".".join(filename.parts)
                module: types.ModuleType = import_module(name, package=package)
                if hasattr(module, "event_message"):
                    bot.manual_event_message.append(module.event_message)
            except Exception as e:
                logger.error(f"Listener '{filename[:-3]}' failed to load: {e}", extra={"locals": locals()})

    @staticmethod
    def load_routines(bot: Gorenmu, path: pathlib.Path) -> None:
        for filename in path.iterdir():
            if not filename.suffix == ".py" or filename.name.startswith("__"):
                continue
            try:
                local: str = os.path.join(path, filename.name)
                name: str = local[:-3].replace("/", ".")
                package: str = ".".join(filename.parts)
                module: types.ModuleType = import_module(name, package=package)
                routine: Routine = module.routine
                bot.routines.append(routine)
            except Exception as e:
                logger.error(f"Routine '{filename.name[:-3]}' failed to load: {e}", extra={"locals": locals()})

    @staticmethod
    async def load_cogs(bot: Gorenmu, base: str) -> None: # TODO: Mudar para lidar com os novos comandos
        cogs = pathlib.Path(base)
        try:
            for cog in cogs.iterdir():
                cog: pathlib.Path
                if ".example" in cog.name:
                    continue
                if cog.is_file():
                    continue
                for folder in cog.iterdir():
                    if folder.name == "__pycache__" or folder.name == "data":
                        continue
                    if "commands" in folder.name or "command" in folder.name:
                        await CommandHandler.load_commands(bot, folder.joinpath())
                    elif "manual_event_message" in folder.name:
                        CommandHandler.load_manual_event_message(bot, folder.joinpath())
                    elif "routines" in folder.name:
                        CommandHandler.load_routines(bot, folder.joinpath())
            CommandHandler.start_routines(bot)
        except Exception as e:
            logger.error(e)

    @staticmethod
    async def reload_cogs(bot: Gorenmu, base: str = "bot/cogs") -> None:
        CommandHandler.stop_routines(bot)
        cogs = pathlib.Path(base)
        for cog in cogs.iterdir():
            cog: pathlib.Path
            if ".example" in cog.name:
                continue
            if cog.is_file():
                continue
            for folder in cog.iterdir():
                if folder.name == "__pycache__" or folder.name == "data":
                    continue
                if "commands" in folder.name or "command" in folder.name:
                    await CommandHandler.load_commands(bot, folder.joinpath())
                if "manual_event_message" in folder.name:
                    CommandHandler.load_manual_event_message(bot, folder.joinpath())
                if "routines" in folder.name:
                    CommandHandler.load_routines(bot, folder.joinpath())
        CommandHandler.start_routines(bot)

    @staticmethod
    def load_language(ctx: Context):
        channel = ctx.channel.name
        channel = ctx.bot.channels[channel]
        ctx.translations = ctx.bot.TranslationManager.get_translations(ctx.user.language or channel.language or "en")
        # ctx.decorators = ctx.bot.TranslationManager.get_decorator(ctx.user.language or channel.language or "en")
