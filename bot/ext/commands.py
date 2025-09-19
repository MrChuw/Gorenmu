# -*- coding: utf-8 -*-
from __future__ import annotations

import asyncio
from abc import ABC
from collections.abc import Callable, Coroutine, Iterable
from functools import partial
from typing import (
    TYPE_CHECKING,
    Any,
    Concatenate,
    Generic,
    Optional,
    ParamSpec,
    Self,
    Sequence,
    TypeAlias,
    TypeVar,
    Union,
)

from twitchio import ChatMessage, User
from twitchio.ext.commands import AutoBot, Bucket, BucketType
from twitchio.ext.commands import Command as TwitchioCommand
from twitchio.ext.commands import CommandErrorPayload, Component, Cooldown
from twitchio.ext.commands import Group as TwitchioGroup
from twitchio.ext.commands import cooldown
from twitchio.ext.commands.exceptions import CommandError
from twitchio.ext.commands.types_ import Component_T
from twitchio.ext.routines import routine

from bot.translations import BaseCommand

T = TypeVar("T")
Coro: TypeAlias = Coroutine[Any, Any, None]
CoroC: TypeAlias = Coroutine[Any, Any, bool]
if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.ext import Context, TranslationBase

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
    "CommandErrorPayload",
    "CustomComponent",
    "AutoBot",
)

max_message_len = 450
minimum_delay_messages = 0.2


class Command(TwitchioCommand):
    decorator_path: str
    docs: Callable[[], dict[str, dict[str, str]]]
    template: bool
    pipeble: bool
    component: CustomComponent

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.decorators: dict[str, BaseCommand] = {}

    def command(
        self,
        name: str | None = None,
        aliases: list[str] | None = None,
        extras: dict[Any, Any] | None = None,
        pipeble: bool = True,
        **kwargs: Any,
    ):
        return super().command(name=name, aliases=aliases, extras=extras, pipeble=pipeble, **kwargs)  # NOQA

    @property
    def all_guards(self):
        return self.component.guards() + self.guards

    async def dispatch_error(self, context: Context, exception: CommandError) -> None:
        await self._dispatch_error(context, exception)

    @property
    def buckets(self) -> list[Bucket]:
        return self._buckets

    @property
    def per(self):
        return self._buckets[0]._cooldown._per  # NOQA

    @property
    def rate(self):
        return self._buckets[0]._cooldown._rate  # NOQA


class CustomComponent(Component):
    translations: TranslationBase = None

    def __new__(cls, *args, **kwargs) -> Self:
        self: Self = super().__new__(cls, *args, **kwargs)
        bot: Gorenmu = args[0] if args else kwargs.get("bot")
        rate = getattr(self, "cooldown_rate", 10)
        per = getattr(self, "cooldown_per", 3)
        key = getattr(self, "cooldown_key", BucketType.user)
        bucket_: Bucket[Context] = Bucket.from_cooldown(base=Cooldown, key=key, **{"per": per, "rate": rate})
        category_name: str = getattr(self, "name", self.__class__.__name__)
        category_name = category_name.removesuffix("Cmd").removesuffix("Cmds")
        self.inject_events(bot, cls, self, category_name)
        for command_name in self.__all_commands__:
            command_: Command = self.__all_commands__[command_name]
            if hasattr(command_, "commands"):
                for name in command_.commands:
                    self._extras(command_.commands[name], bucket_, bot)
                    bot.docs[category_name][command_.commands[name].name] = command_.commands[name].docs
            self._extras(command_, bucket_, bot)
            bot.docs[category_name][command_.name] = command_.docs
        return self

    @staticmethod
    def _extras(new_command: Command, bucket_, bot: Gorenmu):
        if len(new_command._buckets) == 0:  # NOQA
            new_command._buckets.append(bucket_)  # NOQA

        def docs():
            if new_command.template:
                return bot.docs_handler.template_description(new_command)
            else:
                return bot.docs_handler.normal_description(new_command)

        new_command.docs = docs

    @staticmethod
    def inject_events(bot, cls, self, category_name):
        if category_name in bot.manual_events:
            bot.manual_events[category_name].clear()
        for name, member in cls.__dict__.items():
            event_name = getattr(member, "_event_info", None)
            if not event_name:
                continue
            injected = partial(member, self)
            bot.manual_events[category_name][event_name][name] = injected


def base_decorator(base: str, template=False) -> Callable[[Command], Command]:
    def decorator(command: Command) -> Command:  # NOQA
        command.decorator_path = base
        command.template = template
        return command

    return decorator


def command(
    name: str | None = None,
    aliases: list[str] | None = None,
    extras: dict[Any, Any] | None = None,
    pipeble: bool = True,
    **kwargs: Any,
) -> Any:
    def wrapper(
        func: Callable[Concatenate[Component_T, Context, P], Coro] | Callable[Concatenate[Context, P], Coro],
    ) -> Command:
        if isinstance(func, Command):
            raise ValueError(f'Callback "{func._callback}" is already a Command.')  # NOQA

        if not asyncio.iscoroutinefunction(func):
            raise TypeError(f'Command callback for "{func.__qualname__}" must be a coroutine function.')

        func_name = func.__name__
        name_ = name.strip().replace(" ", "") or func_name if name else func_name
        command_ = Command(name=name_, callback=func, aliases=aliases or [], extras=extras or {}, **kwargs)
        command_.pipeble = pipeble
        return command_

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


class Group(TwitchioGroup):
    component: CustomComponent

    def command(
        self,
        name: str | None = None,
        aliases: list[str] | None = None,
        extras: dict[Any, Any] | None = None,
        pipeble: bool = True,  # NOQA
        **kwargs: Any,
    ) -> Any:
        def wrapper(
            func: Callable[Concatenate[Component_T, Context, P], Coro] | Callable[Concatenate[Context, P], Coro],
        ) -> Command:
            new = command(name=name, aliases=aliases, extras=extras, parent=self, pipeble=pipeble, **kwargs)(func)

            self.add_command(new)
            return new

        return wrapper

    def get_command(self, name: str, /) -> Optional[Command | Group]:
        return super().get_command(name)


def group(
    name: str | None = None, aliases: list[str] | None = None, extras: dict[Any, Any] | None = None, **kwargs: Any
) -> Callable[[Command], Command]:
    def wrapper(
        func: Callable[Concatenate[Component_T, Context, P], Coro] | Callable[Concatenate[Context, P], Coro],
    ) -> Group:
        if isinstance(func, Command):
            raise ValueError(f'Callback "{func._callback.__name__}" is already a Command.')  # NOQA

        if not asyncio.iscoroutinefunction(func):
            raise TypeError(f'Group callback for "{func.__qualname__}" must be a coroutine function.')

        func_name = func.__name__
        name_ = name.strip().replace(" ", "") or func_name if name else func_name

        return Group(name=name_, callback=func, aliases=aliases or [], extras=extras or {}, **kwargs)

    return wrapper


def event_handler(event_name: str):
    def decorator(func: Callable):
        func._event_info = event_name  # type: ignore
        return func

    return decorator


# def event_handler(event_name: str):
#     def decorator(func: Callable):
#         async def wrapper(self, *args, **kwargs):
#             return await func(self, *args, **kwargs)
#         wrapper._event_info = event_name
#         return wrapper
#     return decorator
