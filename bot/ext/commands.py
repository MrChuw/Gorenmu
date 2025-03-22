# -*- coding: utf-8 -*-
from __future__ import annotations

import asyncio
import re
from typing import TYPE_CHECKING, Any, Concatenate, Type, ParamSpec, TypeAlias, TypeVar, Self, overload
from collections.abc import Callable, Coroutine

from collections.abc import Iterable



from bot.models import User as UserModel, Alias
from bot.translations import Decorators, BaseCommand
from bot.translations import Response
from bot.translations.base_decorators import inject_translations

import twitchio
from twitchio.ext.commands.exceptions import (CommandNotFound, CommandError, CommandHookError,
                                              CommandInvokeError, ConversionError)
from twitchio.ext.commands.core import CommandErrorPayload
from twitchio.ext.commands.types_ import Component_T


from twitchio import User, ChatMessage
from twitchio.ext.commands import (
    Bot as TwitchioBot, Bucket, Command as TwitchioCommand, Context as TwitchioContext, cooldown,
    MissingRequiredArgument, Cooldown, BucketType, Component, group
)
from twitchio.ext.routines import routine





T = TypeVar('T')
Coro: TypeAlias = Coroutine[Any, Any, None]
CoroC: TypeAlias = Coroutine[Any, Any, bool]
if TYPE_CHECKING:
    from bot.bot import Gorenmu

    PrefixT: TypeAlias = str | Iterable[str] | Callable[[Gorenmu, ChatMessage], Coroutine[Any, Any, str | Iterable[str]]]

    P = ParamSpec("P")
else:
    P = TypeVar("P")


max_message_len = 450
minimum_delay_messages = 0.2

__all__ = (
        "Bot", "ChatMessage", "Bucket", "Context", "User",
        "cooldown", "routine", "base_decorator", "usage", "helper", "Command",
        "Component", "BucketType", "guard", "group"
        )


class Command(TwitchioCommand):
    decorators: dict[str, BaseCommand]
    decorators_original: Decorators
    _cooldowns: Cooldown
    docs: dict[str, dict[str, str]]

    def command(self, name: str | None = None, aliases: list[str] | None = None, extras: dict[Any, Any] | None = None,
                **kwargs: Any
                ):
        return super().command(name=name, aliases=aliases, extras=extras, **kwargs)  # NOQA


class Bot(TwitchioBot):
    async def get_prefix(self: Gorenmu, message: ChatMessage):
        if message.subscription_type == 'user.whisper.message':
            return "+"
        return self.channels[message.broadcaster.name].prefix

    async def get_context(self, message: ChatMessage | twitchio.Whisper, *, cls: Context = None):
        """Get a Context object from a message.

        Parameters
        ----------
        message: :class:`.Message`
            The message object to get context for.
        cls
            The class to return. Defaults to Context. Its constructor must take message, prefix, valid, and bot
            as arguments.

        Returns
        ---------
        An instance of cls.

        Raises
        ---------
        :class:`.CommandNotFound` No valid command was passed
        """
        if "\x01ACTION " in message.text:
            message.text = message.text.replace("\x01ACTION ", "").replace("\x01", "")
        prefix = await self.get_prefix(message)
        invoke_by = None
        if message and message.text and prefix in message.text:
            invoke_by = message.text.partition(" ")[0][len(prefix):].lower()
        context = Context(message=message, bot=self, prefix=prefix, invoke_by=invoke_by)
        return context

    async def invoke(self, context: Context, *, index=0) -> Response | None | bool:  # NOQA
        try:
            return await context.invoke()
        except CommandError as e:
            payload = CommandErrorPayload(context=context, exception=e)
            self.dispatch("command_error", payload=payload)


class Context(TwitchioContext):
    user: UserModel
    bot: Gorenmu
    # translations: Translations
    # decorators:  Decorators
    command: Command
    _command: Command
    invoke_by: str | None = None

    def __init__(self, message: ChatMessage, *, bot: Bot, prefix: str, invoke_by: str | None):
        super().__init__(message, bot=bot)
        self._prefix: str | None = prefix
        self.invoke_by: str | None = invoke_by

    def __iter__(self):
        yield "author", self.author.name if self.author and self.author.name else None
        yield "channel", self.channel.name if self.channel and self.channel.name else None
        yield "message", self.message.text if self.message and self.message.text else None
        yield "command", self.command.name if self.command and self.command.name else None

    @staticmethod
    async def extract_response(response: Response):
        if response:
            handle = response.handle
        else:
            handle = None
        if response.response_string:
            response_str = response.response_string
        else:
            response_str = None
        if response.response_list:
            response_list = response.response_list
        else:
            response_list = None
        return handle, response_str, response_list, response.success

    @staticmethod
    async def handle_response(ctx: Context, full_response: str):
        chunks = []
        while len(full_response) > max_message_len:
            index_space = full_response.rfind(" ", 0, max_message_len)
            if index_space == -1:
                chunks.append(full_response[:max_message_len])
                full_response = full_response[max_message_len:]
            else:
                chunks.append(full_response[:index_space])
                full_response = full_response[index_space + 1:]
        chunks.append(full_response)
        for chunk in chunks:
            await ctx.reply(chunk)
            await asyncio.sleep(minimum_delay_messages)

    @staticmethod
    async def handle_echo(ctx: Context, response_str: str):
        if len(response_str) < max_message_len:
            return await ctx.reply(f"{response_str}")
        part1 = response_str[:max_message_len]
        part2 = response_str[max_message_len:]
        await ctx.reply(f"{part1}")
        await asyncio.sleep(0.5)
        await ctx.reply(f"{part2}")

    @staticmethod
    async def handle_banwords(ctx: Context, response_str: str):
        banwords = ctx.bot.channels[ctx.channel.name].banwords
        user_handler = ctx.user.nickname or ctx.author.name
        for word in banwords.keys():
            if word in response_str:
                tamanho = len(word)
                asteriscos = "".join("*" for _ in range(tamanho))
                response_str = response_str.replace(word, asteriscos)
            if word in ctx.user.nickname:
                user_handler = ctx.author.name
        return response_str, user_handler

    async def handle_response_list(self, ctx: Context, response_list: list[str], handle: str | None):
        for response in response_list:
            response_str, user_handler = await self.handle_banwords(ctx=ctx, response_str=response)
            full_response: str = f"{user_handler} {response_str}"
            if handle == "echo":
                await self.handle_echo(ctx=ctx, response_str=response_str)
            else:
                await self.handle_response(ctx=ctx, full_response=full_response)
            await asyncio.sleep(minimum_delay_messages)

    async def send_response(self, ctx: Context, user_handler: str, response_str: str):
        full_response: str = f"{user_handler} {response_str}"
        if len(full_response) < max_message_len:
            return await ctx.reply(full_response)
        else:
            await self.handle_response(ctx=ctx, full_response=full_response)

    async def response(self, response: Response) -> None | bool:
        ctx: Context = response.ctx
        if ctx.bot.channels[ctx.channel.name].online is False:
            return False
        handle, response_str, response_list, success = await self.extract_response(response)
        response_str, user_handler = await self.handle_banwords(ctx, response_str)

        if handle == "echo" and not response_list:
            await self.handle_echo(ctx=ctx, response_str=response_str)
        if response_str:
            await self.send_response(ctx, user_handler, response_str)
        if response_list:
            await self.handle_response_list(ctx, response_list, handle)

    async def simple_response(self, ctx: Context, response: str, handle: str = None) -> None | bool:  # NOQA
        if ctx.bot.channels[ctx.channel.name].online is False:
            return False
        response_str = response
        response_str, user_handler = await self.handle_banwords(ctx, response_str)

        if handle == "echo":
            await self.handle_echo(ctx=ctx, response_str=response_str)
        await self.send_response(ctx, user_handler, response_str)

    async def pipe_handler(self, external_ctx: Context, message: ChatMessage):
        response_str = ""
        # translations = external_ctx.bot.TranslationManager.get_translations(external_ctx.user.language or "en")
        # translation = translations.Exceptions.ResponseExceptions
        translation = external_ctx.user.translations.Exceptions.ResponseExceptions
        message.text = message.text.replace(" | ", f" | {external_ctx.prefix}")
        original_message = message
        response: Response | None = None
        for command in message.text.split(" | "):  # NOQA
            message = original_message
            if "{output}" in command:  # NOQA
                message.text = command.replace("{output}", response_str)  # NOQA
            else:
                message.text = f"{command} {response_str}"  # NOQA
            ctx = await self.bot.get_context(message)
            ctx.user = external_ctx.user
            ctx.bot.CommandHandler.load_language(ctx)
            response: Response = await self.bot.invoke(ctx)  # NOQA
            if not response:
                return await self.simple_response(ctx, response_str)
            if not response.pipe:
                await self.simple_response(ctx, translation.command_not_pipeble)
                return await self.response(response)
            if not response.success:
                await self.simple_response(ctx, translation.error_on_command.format(ctx.command.name))  # NOQA
                await self.simple_response(ctx, translation.pipe_response.format(response_str))
                break
            response_str = response.response_string
        if response:
            await self.response(response)

    async def alias_handler(self, external_ctx: Context, message: ChatMessage):
        args: list[str] = message.content.replace(f"{external_ctx.prefix}{external_ctx.prefix}", f"").split()
        name: str = args.pop(0)
        alias = await Alias.get_or_none(user=external_ctx.user, name=name, deleted=False)
        if not alias.command:  # NOQA
            alias = await alias.parent
        if not alias:
            return None
        message.content = f"{external_ctx.prefix}{alias.invocation} {' '.join(alias.arguments)}"
        # Add `m_user` for when the commando is invoked on a response.
        if "{channel}" in message.content:
            message.content = message.content.replace("{channel}", external_ctx.channel.name)
        if "{user}" in message.content:
            message.content = message.content.replace("{user}", external_ctx.user.name)
        if args:
            message.content = format_content(message.content, args)
        if " | " in message.content:
            return await self.pipe_handler(external_ctx, message)
        else:
            ctx = await self.bot.get_context(message)
            ctx.user = external_ctx.user
            ctx.bot.CommandHandler.load_language(ctx)
            return await self.bot.invoke(ctx)

    async def invoke(self) -> Response | bool:
        if not self.prefix or not self.is_valid:
            return False
        if not self.command:
            self._get_command()

        if not self.is_valid():
            return False

        if not self._command:
            raise CommandNotFound(f'The command "{self._invoked_with}" was not found.')

        self.bot.dispatch("command_invoked", self)

        command_result: None | Response = None
        try:
            command_result = await self._command.invoke(self)
        except CommandError as e:
            self._failed = True
            await self._command._dispatch_error(self, e)  # NOQA

        if self._passed_guards:
            try:
                await self._bot.after_invoke(self)
                if self._component:
                    await self._component.component_after_invoke(self)
            except Exception as e:
                payload = CommandErrorPayload(context=self, exception=CommandHookError(str(e), e))
                self.bot.dispatch("command_error", payload=payload)
                return False

        if not self._failed:
            self.bot.dispatch("command_completed", self)

        return command_result


class CustomComponent(Component):
    def __new__(cls, *args, **kwargs) -> Self:
        self: Self = super().__new__(cls, *args, **kwargs)
        bot: Gorenmu = args[0]
        translations = bot.TranslationManager
        rate = getattr(self, 'cooldown_rate', 10)
        per = getattr(self, 'cooldown_per', 3)
        key = getattr(self, 'cooldown_key', BucketType.user)
        bucket_: Bucket[Context] = Bucket.from_cooldown(base=Cooldown, key=key, **{'per': per, 'rate': rate})

        for command_name in self.__all_commands__:
            command_ = self.__all_commands__[command_name]
            if command_name in ["alias", "socials"]:
                ...
            self.__all_commands__[command_name] = inject_translations(command_, translations)
            if len(command_._buckets) == 0:  # NOQA
                command_._buckets.append(bucket_)  # NOQA

            if command_.name.lower() in ["afk", "isafk", "rafk"]:  # TODO: Mudar
                command_.docs = bot.docs_handler.afk_description(command_)
            elif command_.name.lower() in ["cookies"]:
                command_.docs = bot.docs_handler.cookies_description(command_)
            elif command_.name.lower() in ["alias"]:
                command_.docs = bot.docs_handler.template_description(command_)
            else:
                command_.docs = bot.docs_handler.normal_description(command_)

        return self


def usage(usage: str) -> Callable[[Command], Command]:  # NOQA
    def decorator(command: Command) -> Command:  # NOQA
        # if type(command) != Command:
        #     raise TypeError(f"Expected 'twitchio.ext.commands.Command', not '{type(command)}'")
        command.usage = usage
        return command

    return decorator


def helper(description: str) -> Callable[[Command], Command]:
    def decorator(command: Command) -> Command:  # NOQA
        # if type(command) != Command:
        #     raise TypeError(f"Expected 'twitchio.ext.commands.Command', not '{type(command)}'")
        command.description = description
        return command

    return decorator


def base_decorator(base: Decorators | Type[T]) -> Callable[[Command], Command]:
    def decorator(command: Command) -> Command:  # NOQA
        command.decorators_original = base
        return command

    return decorator


def format_content(content: str, values: list[str]) -> str:
    def replace_match(match):
        index_str = match.group(0)[1:-1]
        if '+' in index_str:
            return " ".join(values[int(index_str[0]):])
        return values[int(index_str)]

    return re.sub(r'\{\d+(?:\+\d*)?}', replace_match, content)


def command(
    name: str | None = None, aliases: list[str] | None = None, extras: dict[Any, Any] | None = None, **kwargs: Any
) -> Any:
    """|deco|

    A decorator which turns a coroutine into a :class:`~.commands.Command` which can be used in
    :class:`~.commands.Component`'s or added to a :class:`~.commands.Bot`.

    Commands are powerful tools which enable bots to process messages and convert the content into mangeable arguments and
    :class:`~.commands.Context` which is parsed to the wrapped callback coroutine.

    Commands also benefit to such things as :func:`~.guard`'s and the ``before`` and ``after`` hooks on both,
    :class:`~.commands.Component` and :class:`~.commands.Bot`.

    Command callbacks should take in at minimum one parameter, which is :class:`~.commands.Context` and is always
    passed.

    Parameters
    ----------
    name: str | None
        An optional custom name to use for this command. If this is ``None`` or not passed, the coroutine function name
        will be used instead.
    aliases: list[str] | None
        An optional list of aliases to use for this command.
    extras: dict
        A dict of any data which is stored on this command object. Can be used anywhere you have access to the command object,
        E.g. in a ``before`` or ``after`` hook.
    guards_after_parsing: bool
        An optional bool, indicating whether to run guards after argument parsing has completed.
        Defaults to ``False``, which means guards will be checked **before** command arguments are parsed and available.
    cooldowns_before_guards: bool
        An optional bool, indicating whether to run cooldown guards after all other guards succeed.
        Defaults to ``False``, which means cooldowns will be checked **after** all guards have successfully completed.
    bypass_global_guards: bool
        An optional bool, indicating whether the command should bypass the :meth:`.Bot.global_guard`.
        Defaults to ``False``.

    Examples
    --------

    .. code:: python3

        # When added to a Bot or used in a component you can invoke this command with your prefix, E.g:
        # !hi or !howdy

        @commands.command(name="hi", aliases=["hello", "howdy"])
        async def hi_command(ctx: commands.Context) -> None:
            ...

    Raises
    ------
    ValueError
        The callback being wrapped is already a command.
    TypeError
        The callback must be a coroutine function.
    """

    def wrapper(
        func: Callable[Concatenate[Component_T, Context, P], Coro] | Callable[Concatenate[Context, P], Coro],
    ) -> Command[Any, ...]:
        if isinstance(func, Command):
            raise ValueError(f'Callback "{func._callback}" is already a Command.')  # type: ignore

        if not asyncio.iscoroutinefunction(func):
            raise TypeError(f'Command callback for "{func.__qualname__}" must be a coroutine function.')

        func_name = func.__name__
        name_ = name.strip().replace(" ", "") or func_name if name else func_name

        return Command(name=name_, callback=func, aliases=aliases or [], extras=extras or {}, **kwargs)

    return wrapper


def guard(*predicates: bool | (Callable[..., bool] | Callable[..., CoroC])) -> Any:
    """A function which takes in a predicate as a either a standard function *or* coroutine function which should
    return either ``True`` or ``False``, and adds it to your :class:`~.commands.Command` as a guard.

    The predicate function should take in one parameter, :class:`.commands.Context`, the context used in command invocation.

    If the predicate function returns ``False``, the chatter will not be able to invoke the command and an error will be
    raised. If the predicate function returns ``True`` the chatter will be able to invoke the command,
    assuming all the other guards also pass their predicate checks.

    Guards can also raise custom exceptions, however your exception should inherit from :exc:`~.commands.GuardFailure` which
    will allow your exception to propagate successfully to error handlers.

    Any number of guards can be used on a :class:`~.commands.Command` and all must pass for the command to be successfully
    invoked.

    All guards are executed in the specific order displayed below:

    - **Global Guard:** :meth:`.commands.Bot.global_guard`

    - **Component Guards:** :meth:`.commands.Component.guard`

    - **Command Specific Guards:** The command specific guards, E.g. by using this or other guard decorators on a command.

    .. note::

        Guards are checked and ran **after** all command arguments have been parsed and converted, but **before** any
        ``before_invoke`` hooks are ran.

    It is easy to create simple decorator guards for your commands, see the examples below.

    Some built-in helper guards have been premade, and are listed below:

    - :func:`~.commands.is_staff`

    - :func:`~.commands.is_broadcaster`

    - :func:`~.commands.is_moderator`

    - :func:`~.commands.is_vip`

    - :func:`~.commands.is_elevated`

    Example
    -------

    .. code:: python3

        def is_cool():
            def predicate(ctx: commands.Context) -> bool:
                return ctx.chatter.name.startswith("cool")

            return commands.guard(predicate)

        @is_cool()
        @commands.command()
        async def cool(self, ctx: commands.Context) -> None:
            await ctx.reply("You are cool...!")

    Raises
    ------
    GuardFailure
        The guard predicate returned ``False`` and prevented the chatter from using the command.
    """


    def wrapper(func: Any) -> Any:
        if isinstance(func, Command):
            func._guards.extend(predicates)  # NOQA

        else:
            try:
                func.__command_guards__.extend(predicates)  # NOQA
            except AttributeError:
                func.__command_guards__ = list(predicates)  # NOQA

        return func  # type: ignore

    return wrapper




