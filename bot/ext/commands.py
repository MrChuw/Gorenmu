from __future__ import annotations

import asyncio
from collections.abc import Callable, Coroutine, Iterable, Sequence
from functools import partial
from typing import TYPE_CHECKING, Any, Concatenate, ParamSpec, Self, TypeVar

from twitchio import ChatMessage, User
from twitchio.ext.commands import (
    AutoBot,
    Bucket,
    BucketType,
    CommandErrorPayload,
    Component,
    Cooldown,
    cooldown,
)
from twitchio.ext.commands import Command as TwitchioCommand
from twitchio.ext.commands import Group as TwitchioGroup
from twitchio.ext.commands.exceptions import CommandError
from twitchio.ext.commands.types_ import Component_T
from twitchio.ext.routines import routine

T = TypeVar("T")
type Coro = Coroutine[Any, Any, None]
type CoroC = Coroutine[Any, Any, bool]
if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.ext import Context, TranslationBase

    type PrefixT = str | Iterable[str] | Callable[[Gorenmu, ChatMessage], Coroutine[Any, Any, str | Iterable[str]]]

    P = ParamSpec("P")

__all__ = (
    "AutoBot",
    "Bucket",
    "BucketType",
    "ChatMessage",
    "Command",
    "CommandErrorPayload",
    "Component",
    "CustomComponent",
    "Group",
    "User",
    "cooldown",
    "guard",
    "routine",
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
        bucket_: Bucket[Context] = Bucket.from_cooldown(base=Cooldown, key=key, **{"per": per, "rate": rate})  # NOQA
        category_name: str = getattr(self, "name", self.__class__.__name__)
        category_name = category_name.removesuffix("Cmd").removesuffix("Cmds")
        self.inject_events(bot, cls, self, category_name)
        for command_name in self.__all_commands__:
            command_: Command = self.__all_commands__[command_name]
            if hasattr(command_, "commands"):
                for name in command_.commands:
                    if len(command_.commands[name]._buckets) == 0:  # NOQA
                        command_.commands[name]._buckets.append(bucket_)  # NOQA
            if len(command_._buckets) == 0:  # NOQA
                command_._buckets.append(bucket_)  # NOQA
        return self

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


def command(
    name: str | None = None,
    aliases: list[str] | None = None,
    extras: dict[Any, Any] | None = None,
    pipeble: bool = True,
    **kwargs: Any,
) -> Any:
    def wrapper(
        func: (Callable[Concatenate[Component_T, Context, P], Coro] | Callable[Concatenate[Context, P], Coro]),
    ) -> Command:
        if isinstance(func, Command):
            raise ValueError(f'Callback "{func._callback}" is already a Command.')  # NOQA

        if not asyncio.iscoroutinefunction(func):
            raise TypeError(f'Command callback for "{func.__qualname__}" must be a coroutine function.')

        func_name = func.__name__
        name_ = name.strip().replace(" ", "") or func_name if name else func_name
        command_ = Command(
            name=name_,
            callback=func,
            aliases=aliases or [],
            extras=extras or {},
            **kwargs,
        )
        command_.pipeble = pipeble
        return command_

    return wrapper


def guard(
    predicates: (Callable[..., bool] | Callable[..., CoroC] | Sequence[Callable[..., Any]]),
) -> Any:
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
            func: (Callable[Concatenate[Component_T, Context, P], Coro] | Callable[Concatenate[Context, P], Coro]),
        ) -> Command:
            new = command(
                name=name,
                aliases=aliases,
                extras=extras,
                parent=self,
                pipeble=pipeble,
                **kwargs,
            )(func)

            self.add_command(new)
            return new

        return wrapper

    def get_command(self, name: str, /) -> Command | Group | None:
        return super().get_command(name)


def group(
    name: str | None = None,
    aliases: list[str] | None = None,
    extras: dict[Any, Any] | None = None,
    **kwargs: Any,
) -> Callable[[Command], Command]:
    def wrapper(
        func: (Callable[Concatenate[Component_T, Context, P], Coro] | Callable[Concatenate[Context, P], Coro]),
    ) -> Group:
        if isinstance(func, Command):
            raise ValueError(f'Callback "{func._callback.__name__}" is already a Command.')  # NOQA

        if not asyncio.iscoroutinefunction(func):
            raise TypeError(f'Group callback for "{func.__qualname__}" must be a coroutine function.')

        func_name = func.__name__
        name_ = name.strip().replace(" ", "") or func_name if name else func_name

        return Group(
            name=name_,
            callback=func,
            aliases=aliases or [],
            extras=extras or {},
            **kwargs,
        )

    return wrapper  # NOQA


def event_handler(event_name: str):
    def decorator(func: Callable):
        func._event_info = event_name  # type: ignore
        return func

    return decorator
