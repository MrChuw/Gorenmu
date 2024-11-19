# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import pathlib
import types
from importlib import import_module, reload
from typing import TYPE_CHECKING

from loguru import logger
from twitchio.ext.commands import Bucket
from bot.ext import Routine
from bot.translations import TranslationManager

if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.ext import Context, Command

from bot.utils.command_checks import Check


def get_translations(command: Command):
    translations = TranslationManager()
    translations_decorators = {}
    fallback = translations.languages["en"].decorators
    categories = ["", "NSFW", "Dev"]

    for lang, lang_data in translations.languages.items():
        translation = lang_data.decorators

        decorators_dict = translation.__dict__


        for category in categories:
            decorators = translation.decorators.get(category, translation.decorators)
            if command.name.lower() in decorators:
                translations_decorators[lang] = decorators[command.name.lower()]
                break
        else:
            for category in categories:
                fallback_decorators = fallback.get(category, translation.decorators)
                if command.name.lower() in fallback_decorators:
                    translations_decorators[lang] = fallback_decorators[command.name.lower()]
                    break

    command.decorators = translations_decorators
    return command


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
    DEFAULT_COOLDOWN_BUCKET = Bucket.user

    @staticmethod
    def start_routines(self: Gorenmu) -> None:  # TODO: Melhorar as mensagens.
        for routine in self.routines:
            routine.start(self)

    @staticmethod
    def stop_routines(self: Gorenmu) -> None:  # TODO: Melhorar as mensagens.
        try:
            for routine in self.routines:
                routine.cancel()
        except Exception as e:
            logger.error(e)

    @staticmethod
    def load_commands(bot: Gorenmu, path: pathlib.Path) -> None:
        for filename in path.iterdir():
            if not filename.suffix == ".py" or filename.name.startswith("__"):
                continue
            try:
                # if filename.name in ['imgur.py', 'imgur_repeated.py', 'nada.py', 'reload.py']:
                if filename.name in ['afk.py']:
                    pass
                local: str = os.path.join(path, filename.name)
                name: str = local[:-3].replace("/", ".")
                package: str = ".".join(filename.parts)
                module: types.ModuleType = import_module(name, package=package)
                command: Command = module.command
                command = get_translations(command)
                # command.docs = module.dynamic_description(command, bot)
                if "disabled" in module.__dict__:
                    continue
                if command.name not in bot.commands:
                    bot.add_command(command)
                else:
                    module = reload(module)
                    command: Command = module.command
                    bot.remove_command(command.name)
                    bot.add_command(command)

            except Exception as e:
                logger.error(f"Command '{filename.name[:-3]}' failed to load: {e} in {filename.joinpath()}",
                             extra={"locals": locals()}, )

    @staticmethod
    def load_event_message_listeners(bot: Gorenmu, path: pathlib.Path) -> None:
        for filename in path.iterdir():
            if not filename.suffix == ".py" or filename.name.startswith("__"):
                continue
            try:
                local: str = os.path.join(path, filename.name)
                name: str = local[:-3].replace("/", ".")
                package: str = ".".join(filename.parts)
                module: types.ModuleType = import_module(name, package=package)
                bot.event_message_listeners.append(module.listener)
            except Exception as e:
                logger.error(f"Listener '{filename[:-3]}' failed to load: {e}", extra={"locals": locals()})

    @staticmethod
    def load_routines(bot: Gorenmu, path: pathlib.Path) -> None:
        bot.routines = []
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
    def load_cogs(bot: Gorenmu, base: str) -> None:
        global_checks = [Check.online, Check.enabled, Check.banword]
        [bot.check(check) for check in global_checks]
        cogs = pathlib.Path(base)
        try:
            for cog in cogs.iterdir():
                if ".example" in cog.name:
                    continue
                for folder in cog.iterdir():
                    if folder.name == "__pycache__" or folder.name == "data":
                        continue
                    if "commands" in folder.name or "command" in folder.name:
                        CommandHandler.load_commands(bot, folder.joinpath())
                    elif "event_message_listeners" in folder.name:
                        CommandHandler.load_event_message_listeners(bot, folder.joinpath())
                    elif "routines" in folder.name:
                        CommandHandler.load_routines(bot, folder.joinpath())
            CommandHandler.start_routines(bot)
        except Exception as e:
            logger.error(e)

    @staticmethod
    def reload_cogs(bot: Gorenmu, base: str = "bot/cogs") -> None:
        CommandHandler.stop_routines(bot)
        cogs = pathlib.Path(base)
        for cog in cogs.iterdir():
            if ".example" in cog.name:
                continue
            for folder in cog.iterdir():
                if folder.name == "__pycache__" or folder.name == "data":
                    continue
                if "commands" in folder.name or "command" in folder.name:
                    CommandHandler.load_commands(bot, folder.joinpath())
                if "event_message_listeners" in folder.name:
                    CommandHandler.load_event_message_listeners(bot, folder.joinpath())
                if "routines" in folder.name:
                    CommandHandler.load_routines(bot, folder.joinpath())
        CommandHandler.start_routines(bot)

    @staticmethod
    def load_language(ctx: Context):
        channel = ctx.channel.name
        channel = ctx.bot.channels[channel]
        ctx.translations = ctx.bot.TranslationManager.get_translations(ctx.user.language or channel.language or "en")
        ctx.decorators = ctx.bot.TranslationManager.get_decorator(ctx.user.language or channel.language or "en")
