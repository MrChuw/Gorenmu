from __future__ import annotations

import asyncio
import re
from collections.abc import Callable, Coroutine, Iterable
from typing import TYPE_CHECKING, Any, ParamSpec, TypeVar

from twitchio.ext.commands.core import CommandErrorPayload
from twitchio.ext.commands.exceptions import (
    CommandError,
    CommandHookError,
    CommandNotFound,
)

from bot.ext import ChatMessage
from bot.models import Alias

T = TypeVar("T")
type Coro = Coroutine[Any, Any, None]
type CoroC = Coroutine[Any, Any, bool]


if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.ext import Context, Response

    type PrefixT = str | Iterable[str] | Callable[[Gorenmu, ChatMessage], Coroutine[Any, Any, str | Iterable[str]]]

    P = ParamSpec("P")
else:
    P = TypeVar("P")


max_message_len = 450
minimum_delay_messages = 0.2


class ContextHandler:
    def __init__(self, bot: Gorenmu):
        self.bot = bot

    @staticmethod
    async def extract_response(response: Response):
        handle = response.handle if response else None
        response_str = response.response_string or None
        response_list = response.response_list or None
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
                full_response = full_response[index_space + 1 :]
        chunks.append(full_response)
        for chunk in chunks:
            await ctx.reply(chunk)
            await asyncio.sleep(minimum_delay_messages)

    async def handle_echo(self, ctx: Context, response_str: str):
        response_str, _ = await self.handle_banwords(ctx=ctx, response_str=response_str)
        if len(response_str) < max_message_len:
            return await ctx.send(f"{response_str}")
        part1 = response_str[:max_message_len]
        part2 = response_str[max_message_len:]
        await ctx.send(f"{part1}")
        await asyncio.sleep(0.5)
        await ctx.send(f"{part2}")
        return None

    @staticmethod
    async def handle_banwords(ctx: Context, response_str: str):
        banned_words = ctx.bot.channels[ctx.channel.name].banwords
        user_display_name = ctx.user.nickname or ctx.author.name
        for word in banned_words:
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            response_str = pattern.sub("*" * len(word), response_str)
            if word.lower() in (ctx.user.nickname or "").lower():
                user_display_name = ctx.author.name
        return response_str, user_display_name

    async def handle_response_list(self, ctx: Context, response_list: list[str], handle: str | None):
        for response in response_list:
            response_str, user_handler = await self.handle_banwords(ctx=ctx, response_str=response)
            if handle == "echo":
                await self.handle_echo(ctx=ctx, response_str=response_str)
            else:
                full_response: str = f"{user_handler} {response_str}"
                await self.handle_response(ctx=ctx, full_response=full_response)
            await asyncio.sleep(minimum_delay_messages)

    async def send_response(self, ctx: Context, user_handler: str, response_str: str):
        full_response: str = f"{user_handler} {response_str}"
        if len(full_response) < max_message_len:
            return await ctx.reply(full_response)
        await self.handle_response(ctx=ctx, full_response=full_response)
        return None

    async def response(self, response: Response) -> None | bool:
        ctx: Context = response.ctx
        if ctx.bot.channels[ctx.channel.name].online is False:
            return False
        handle, response_str, response_list, _ = await self.extract_response(response)
        response_str, user_handler = await self.handle_banwords(ctx, response_str)

        if handle == "echo" and not response_list:
            await self.handle_echo(ctx=ctx, response_str=response_str)
        if response_str and handle != "echo":
            await self.send_response(ctx, user_handler, response_str)
        if response_list:
            await self.handle_response_list(ctx, response_list, handle)
        return None

    async def simple_response(self, ctx: Context, response: str, handle: str | None = None) -> None | bool:
        if ctx.bot.channels[ctx.channel.name].online is False:
            return False
        response_str = response
        response_str, user_handler = await self.handle_banwords(ctx, response_str)

        if handle == "echo":
            await self.handle_echo(ctx=ctx, response_str=response_str)
            return None
        await self.send_response(ctx, user_handler, response_str)
        return None

    async def pipe_handler(self, external_ctx: Context, message: ChatMessage):
        response_str = ""
        translation = external_ctx.command.component.translations.Exceptions
        message.text = message.text.replace(" | ", f" | {external_ctx.prefix}")
        original_message = message
        response: Response | None = None
        for command in message.text.split(" | "):
            message = original_message
            if "{output}" in command:
                message.text = command.replace("{output}", response_str)
            else:
                message.text = f"{command} {response_str}"
            ctx = await self.bot.get_context(message)
            ctx.get_command()
            ctx.user = external_ctx.user
            if not ctx.command.pipeble:
                await self.simple_response(
                    ctx,
                    translation.command_not_pipeble(ctx.command.name).response_string,
                )
                if response_str:
                    await self.simple_response(
                        ctx,
                        translation.pipe_response(response_str).response_string,
                    )
                break

            response: Response = await ctx.invoke()
            if not response and response_str:
                return await self.simple_response(ctx, response_str)
            if not response.success:
                await self.simple_response(
                    ctx,
                    translation.pipe_response_error(ctx.command.name).response_string,
                )
                if response_str:
                    await self.simple_response(
                        ctx,
                        translation.pipe_response(response_str).response_string,
                    )
                if response:
                    response.response_string = f"{translation.pipe_response} {response.response_string}"
                break
            response_str = response.response_string
        if response:
            await self.response(response)
        return None

    async def alias_handler(self, external_ctx: Context, message: ChatMessage):
        args: list[str] = message.content.replace(f"{external_ctx.prefix}{external_ctx.prefix}", "").split()
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

        ctx = await self.bot.get_context(message)
        ctx.user = external_ctx.user
        return await ctx.invoke()

    async def invoke(self, ctx: Context) -> Response | bool:
        if not ctx.prefix or not ctx.is_valid:
            return False
        if not ctx.command:
            ctx.get_command()

        if not ctx.is_valid():
            return False

        if not ctx.command:
            raise CommandNotFound(f'The command "{ctx.invoked_with}" was not found.')

        self.bot.dispatch("command_invoked", self)

        command_result: None | Response = None
        try:
            command_result = await ctx.command.invoke(ctx)
        except CommandError as e:
            ctx._failed = True
            await ctx.command.dispatch_error(ctx, e)

        if ctx.passed_guards:
            try:
                await ctx.bot.after_invoke(ctx)
                if ctx.component:
                    await ctx.component.component_after_invoke(ctx)
            except Exception as e:
                payload = CommandErrorPayload(context=ctx, exception=CommandHookError(str(e), e))
                self.bot.dispatch("command_error", payload=payload)
                return False

        if not ctx.failed:
            self.bot.dispatch("command_completed", self)

        return command_result

    async def setup(self): ...

    async def teardown(self) -> None: ...


def format_content(content: str, values: list[str]) -> str:
    def replace_match(match):
        index_str = match.group(0)[1:-1]
        if "+" in index_str:
            return " ".join(values[int(index_str[0]) :])
        return values[int(index_str)]

    return re.sub(r"\{\d+(?:\+\d*)?}", replace_match, content)
