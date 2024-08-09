# -*- coding: utf-8 -*-
from __future__ import annotations

import asyncio
from typing import Callable, TYPE_CHECKING

from twitchio import Channel, Message, User
from twitchio.ext.commands import (
    BadArgument, Bot, Bucket, Cog, Command as TwitchioCommand, Context as TwitchioContext, cooldown,
    MissingRequiredArgument, command
)
from twitchio.ext.routines import routine

from bot.models import User as UserModel
from bot.translations import EnUsTranslations
from bot.translations import EnUsDecorators
from bot.translations import Response
from bot.translations.en_us.decorators import BaseDecorator

if TYPE_CHECKING:
    from bot.bot import Gorenmu

max_message_len = 450
minimum_delay_messages = 0.1

__all__ = (
        "Bot", "Bucket", "Channel", "Cog", "Context", "Message", "User", "check", "TwitchioCommand", "TwitchioCommand",
        "cooldown", "routine", "base_decorator", "usage", "helper", "command")


class Bot(Bot):
    async def invoke(self, context: Context, *, index=0) -> Response | None:  # NOQA
        if not context.prefix or not context.is_valid:
            return
        context.bot.run_event("command_invoke", context)

        if not context.view:
            return

        async def try_run(func, *, to_command=False):
            try:
                await func
            except Exception as _e:
                if not to_command:
                    context.bot.run_event("error", _e)
                else:
                    context.bot.run_event("command_error", context, _e)

        try:
            args, kwargs = await context.command.parse_args(context, context.command._instance, context.view.words,
                                                            index=index  # NOQA
                                                            )
        except (MissingRequiredArgument, BadArgument) as e:
            if self.event_error:
                args_ = ([context.command._instance, context] if context.command._instance else [context]  # NOQA
                         )
                await try_run(self.event_error(*args_, e))  # NOQA

            context.bot.run_event("command_error", context, e)
            return

        context.args, context.kwargs = args, kwargs
        check_result = await context.command.handle_checks(context)

        if check_result is not True:
            context.bot.run_event("command_error", context, check_result)
            return
        limited = context.command._run_cooldowns(context)  # NOQA

        if limited:
            context.bot.run_event("command_error", context, limited[0])
            return
        instance = context.command._instance  # NOQA
        args = [instance, context] if instance else [context]
        await try_run(context.bot.global_before_invoke(context))

        if context.command._before_invoke:  # NOQA
            await try_run(context.command._before_invoke(*args), to_command=True)  # NOQA

        callback_result = None
        try:
            callback_result = await context.command._callback(  # NOQA
                    *args, *context.args, **context.kwargs
            )
        except Exception as e:
            if self.event_error:
                await try_run(self.event_error(*args, e))  # NOQA
            context.bot.run_event("command_error", context, e)
        else:
            context.bot.run_event("command_complete", context)

        if context.command._after_invoke:  # NOQA
            await try_run(context.command._after_invoke(*args), to_command=True)  # NOQA
        await try_run(context.bot.global_after_invoke(context))

        return callback_result


class Context(TwitchioContext):
    user: UserModel
    bot: Gorenmu
    translations: EnUsTranslations
    decorators: EnUsDecorators

    def __iter__(self):
        yield "author", self.author.name if self.author and self.author.name else None
        yield "channel", self.channel.name if self.channel and self.channel.name else None
        yield "message", self.message.content if self.message and self.message.content else None
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

    async def response(self, response: Response) -> None | bool:  # NOQA
        ctx: Context = response.ctx
        if ctx.bot.channels[ctx.channel.name].online is False:
            return False
        if ctx.bot.channels[ctx.channel.name].prefix == "ƚ":
            return False
        handle, response_str, response_list, success = await self.extract_response(response)
        response_str, user_handler = await self.handle_banwords(ctx, response_str)

        if handle == "echo" and not response_list:
            await self.handle_echo(ctx=ctx, response_str=response_str)

        await self.send_response(ctx, user_handler, response_str)
        if response_list:
            await self.handle_response_list(ctx, response_list, handle)

    async def simple_response(self, ctx: Context, response: str, handle: str = None) -> None | bool:  # NOQA
        if ctx.bot.channels[ctx.channel.name].online is False:
            return False
        if ctx.bot.channels[ctx.channel.name].prefix == "ƚ":
            return False
        response_str = response
        response_str, user_handler = await self.handle_banwords(ctx, response_str)

        if handle == "echo":
            await self.handle_echo(ctx=ctx, response_str=response_str)
        await self.send_response(ctx, user_handler, response_str)

    async def pipe_handler(self, message: Message, external_ctx: Context):
        response_str = ""
        translations = external_ctx.bot.TranslationManager.get_translations(external_ctx.user.language or "pt-br")
        translation = translations.Exceptions.ResponseExceptions()
        message.content = message.content.replace(" | ", f" | {external_ctx.prefix}")
        original_message = message
        response: Response | None = None
        for command in message.content.split(" | "):  # NOQA
            message = original_message
            message.content = f"{command} {response_str}"  # NOQA
            ctx = await self.bot.get_context(message)
            ctx.user = external_ctx.user
            ctx.bot.CommandHandler.load_language(ctx)
            response: Response = await self.bot.invoke(ctx)  # NOQA
            if not response.success:
                await self.simple_response(ctx, translation.error_on_command.format(ctx.command.name))
                await self.simple_response(ctx, translation.pipe_response.format(response_str))
                break
            if not response.pipe:
                await self.simple_response(ctx, translation.command_not_pipeble)
                return await self.response(response)

            response_str = response.response_string
        if response:
            await self.response(response)


def check(check_list: list) -> Callable[[TwitchioCommand], TwitchioCommand]:
    def decorator(command: TwitchioCommand) -> TwitchioCommand:  # NOQA
        for c in check_list:
            command._checks.append(c)  # NOQA
        return command

    return decorator


def usage(usage: str) -> Callable[[TwitchioCommand], TwitchioCommand]:
    def decorator(command: TwitchioCommand) -> TwitchioCommand:
        # if type(command) != Command:
        #     raise TypeError(f"Expected 'twitchio.ext.commands.Command', not '{type(command)}'")
        command.usage = usage
        return command

    return decorator


def helper(description: str) -> Callable[[TwitchioCommand], TwitchioCommand]:
    def decorator(command: TwitchioCommand) -> TwitchioCommand:
        # if type(command) != Command:
        #     raise TypeError(f"Expected 'twitchio.ext.commands.Command', not '{type(command)}'")
        command.description = description
        return command

    return decorator


def base_decorator(base: BaseDecorator) -> Callable[[TwitchioCommand], TwitchioCommand]:
    def decorator(command: TwitchioCommand) -> TwitchioCommand:
        command.decorators = base
        return command

    return decorator
