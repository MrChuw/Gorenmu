# -*- coding: utf-8 -*-
from __future__ import annotations

import asyncio
from collections.abc import Callable, Coroutine, Iterable
from typing import Any, Concatenate, ParamSpec, Self, Sequence, TYPE_CHECKING, TypeAlias, TypeVar, Union

from twitchio import ChatMessage, ChatMessage, User, User
from twitchio.ext.commands import (
    Bucket,
    Bucket,
    BucketType,
    BucketType,
    Command as TwitchioCommand,
    CommandErrorPayload,
    Component,
    Component,
    cooldown,
    cooldown,
    Cooldown,
    group,
    group,
)
from twitchio.ext.commands.exceptions import CommandError
from twitchio.ext.commands.types_ import Component_T
from twitchio.ext.routines import routine, routine

from bot.translations import BaseCommand

T = TypeVar("T")
Coro: TypeAlias = Coroutine[Any, Any, None]
CoroC: TypeAlias = Coroutine[Any, Any, bool]
if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.ext import Context

    PrefixT: TypeAlias = (
        str | Iterable[str] | Callable[[Gorenmu, ChatMessage], Coroutine[Any, Any, str | Iterable[str]]]
    )

    P = ParamSpec("P")

__all__ = (
    "ChatMessage",
    "Bucket",
    "User",
    "cooldown",
    "routine",
    "base_decorator",
    "Command",
    "Component",
    "BucketType",
    "guard",
    "group",
    "CommandErrorPayload",
)

max_message_len = 450
minimum_delay_messages = 0.2


class Command(TwitchioCommand):
    decorator_path: str
    _cooldowns: Cooldown
    docs: Callable[[], dict[str, dict[str, str]]]
    template: bool

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.decorators: dict[str, BaseCommand] = {}

    def command(
        self,
        name: str | None = None,
        aliases: list[str] | None = None,
        extras: dict[Any, Any] | None = None,
        **kwargs: Any,
    ):
        return super().command(name=name, aliases=aliases, extras=extras, **kwargs)  # NOQA

    @property
    def all_guards(self):
        return self.component.guards() + self.guards

    async def dispatch_error(self, context: Context, exception: CommandError) -> None:
        await self._dispatch_error(context, exception)

    @property
    def buckets(self) -> list[Bucket]:
        return self._buckets


class CustomComponent(Component):
    def __new__(cls, *args, **kwargs) -> Self:
        self: Self = super().__new__(cls, *args, **kwargs)
        bot: Gorenmu = args[0] if args else kwargs.get("bot")
        translations = bot.TranslationManager
        rate = getattr(self, "cooldown_rate", 10)
        per = getattr(self, "cooldown_per", 3)
        key = getattr(self, "cooldown_key", BucketType.user)
        bucket_: Bucket[Context] = Bucket.from_cooldown(base=Cooldown, key=key, **{"per": per, "rate": rate})
        category_name: str = getattr(self, "name", self.__class__.__name__)
        category_name = category_name.removesuffix("Cmd").removesuffix("Cmds")

        for command_name in self.__all_commands__:
            command_: Command = self.__all_commands__[command_name]
            if hasattr(command_, "commands"):
                for name in command_.commands:
                    self._extras(command_.commands[name], bucket_, bot, translations)
                    bot.docs[category_name][command_.commands[name].name] = command_.commands[name].docs

            self._extras(command_, bucket_, bot, translations)
            bot.docs[category_name][command_.name] = command_.docs
        return self

    @staticmethod
    def _extras(new_command: Command, bucket_, bot: Gorenmu, translations):
        if len(new_command._buckets) == 0:  # NOQA
            new_command._buckets.append(bucket_)  # NOQA

        def docs():
            if new_command.template:
                return bot.docs_handler.template_description(new_command)
            else:
                return bot.docs_handler.normal_description(new_command)

        new_command.docs = docs


def base_decorator(base: str, template=False) -> Callable[[Command], Command]:
    def decorator(command: Command) -> Command:  # NOQA
        command.decorator_path = base
        command.template = template
        return command

    return decorator


def command(
    name: str | None = None, aliases: list[str] | None = None, extras: dict[Any, Any] | None = None, **kwargs: Any
) -> Any:
    def wrapper(
        func: Callable[Concatenate[Component_T, Context, P], Coro] | Callable[Concatenate[Context, P], Coro],
    ) -> Command[Any, ...]:
        if isinstance(func, Command):
            raise ValueError(f'Callback "{func._callback}" is already a Command.')  # NOQA

        if not asyncio.iscoroutinefunction(func):
            raise TypeError(f'Command callback for "{func.__qualname__}" must be a coroutine function.')

        func_name = func.__name__
        name_ = name.strip().replace(" ", "") or func_name if name else func_name

        return Command(name=name_, callback=func, aliases=aliases or [], extras=extras or {}, **kwargs)

    return wrapper


def guard(predicates: Union[Callable[..., bool], Callable[..., CoroC], Sequence[Callable[..., Any]]]) -> Any:
    if not isinstance(predicates, (list, tuple)):
        predicates = [predicates]

    def wrapper(func: Any) -> Any:
        if isinstance(func, Command):
            func._guards.extend(predicates)  # NOQA
        else:
            try:
                func.__command_guards__.extend(predicates)
            except AttributeError:
                func.__command_guards__ = list(predicates)
        return func  # type: ignore

    return wrapper
