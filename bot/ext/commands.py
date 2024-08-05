# -*- coding: utf-8 -*-
from __future__ import annotations

import asyncio
from typing import Callable, TYPE_CHECKING

from twitchio import Channel, Message, User
from twitchio.cooldowns import RateBucket
from twitchio.ext.commands import (
    BadArgument, Bot, Bucket, Cog, Command, command, Context as TwitchioContext, cooldown, MissingRequiredArgument,
)
from twitchio.ext.routines import routine

from bot.models import User as UserModel
from translations import BaseDecorators
from bot.translations.base import Response
from bot.translations.base.responses import BaseTranslations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class Bot(Bot):  # NOQA
    async def invoke(self, context: Context, *, index=0) -> None:
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
            args, kwargs = await context.command.parse_args(
                context, context.command._instance, context.view.words, index=index
            )
        except (MissingRequiredArgument, BadArgument) as e:
            if self.event_error:
                args_ = (
                    [context.command._instance, context] if context.command._instance else [context]
                )
                await try_run(self.event_error(*args_, e))

            context.bot.run_event("command_error", context, e)
            return

        context.args, context.kwargs = args, kwargs
        check_result = await context.command.handle_checks(context)

        if check_result is not True:
            context.bot.run_event("command_error", context, check_result)
            return
        limited = context.command._run_cooldowns(context)

        if limited:
            context.bot.run_event("command_error", context, limited[0])
            return
        instance = context.command._instance
        args = [instance, context] if instance else [context]
        await try_run(context.bot.global_before_invoke(context))

        if context.command._before_invoke:
            await try_run(context.command._before_invoke(*args), to_command=True)

        callback_result = None
        try:
            callback_result = await context.command._callback(
                *args, *context.args, **context.kwargs
            )
        except Exception as e:
            if self.event_error:
                await try_run(self.event_error(*args, e))
            context.bot.run_event("command_error", context, e)
        else:
            context.bot.run_event("command_complete", context)

        if context.command._after_invoke:
            await try_run(context.command._after_invoke(*args), to_command=True)
        await try_run(context.bot.global_after_invoke(context))

        return callback_result


__all__ = (
    "Bot",
    "Bucket",
    "Channel",
    "Cog",
    "Context",
    "Message",
    "User",
    "check",
    "command",
    "Command",
    "cooldown",
    # "helper",
    "routine",
    # "usage",
    # "base_decorator",
)
RateBucket.MODLIMIT = 1000


class Context(TwitchioContext):
    user: UserModel
    bot: Gorenmu
    translations: BaseTranslations
    decorators: BaseDecorators

    def __iter__(self):
        yield "author", self.author.name if self.author and self.author.name else None
        yield "channel", self.channel.name if self.channel and self.channel.name else None
        yield "message", self.message.content if self.message and self.message.content else None
        yield "command", self.command.name if self.command and self.command.name else None

    # TODO: Fazer logo o novo resposta não se esquecer de adicionar suporte ao response_list.
    #  E tbm caso não tiver response ma tiver response_list
    async def response(self, resposta: Response) -> None | bool:
        ctx: Context = resposta.ctx
        handle = None
        response = resposta

        if not response:
            await ctx.reply(f"{ctx.user.nickname or ctx.author.name} algo deu muito errado.")
            return False

        if response:
            handle = response.handle

        # if not handle or not response:
        #     return

        if ctx.bot.channels[ctx.channel.name].online is False:
            return False
        if ctx.bot.channels[ctx.channel.name].prefix == "ƚ":
            return False

        banwords = ctx.bot.channels[ctx.channel.name].banwords
        for chave in banwords.keys():
            if chave in resposta:
                tamanho = len(chave)
                asteriscos = "".join("*" for _ in range(tamanho))
                response.response_string = response.response_string.replace(chave, asteriscos)

        if handle == "echo":
            if len(response.response) < 450:
                return await ctx.reply(f"{response.response}")
            parte1 = response.response[:450]
            parte2 = response.response[450:]
            await ctx.reply(f"{parte1}")
            await asyncio.sleep(0.5)
            return await ctx.reply(f"{parte2}")

        if len(response.response) < 450:
            return await ctx.reply(f"{ctx.user.nickname or ctx.author.name} {response.response_string}")

        resposta: str = f"{ctx.user.nickname or ctx.author.name} {response.response}"

        tamanho_do_chunk = 450

        chunks = []
        while len(resposta) > tamanho_do_chunk:
            # Procura o último espaço antes da posição de tamanho_do_chunk
            indice_espaco = resposta.rfind(" ", 0, tamanho_do_chunk)

            # Se não houver espaço, divide a string na posição do tamanho do chunk.
            if indice_espaco == -1:
                chunks.append(resposta[:tamanho_do_chunk])
                resposta = resposta[tamanho_do_chunk:]
            else:
                # Divide a string no último espaço antes do tamanho do chunk.
                chunks.append(resposta[:indice_espaco])
                resposta = resposta[indice_espaco + 1 :]

        chunks.append(resposta)

        for chunk in chunks:
            await ctx.reply(chunk)
            if len(chunks) > 5:
                await asyncio.sleep(0.5)
            elif len(chunks) > 10:
                await asyncio.sleep(1)
            else:
                await asyncio.sleep(0.12)

    async def simple_response(self, ctx: Context, resposta: str, handle: str = None) -> None | bool:
        if ctx.bot.channels[ctx.channel.name].online is False:
            return False
        if ctx.bot.channels[ctx.channel.name].prefix == "ƚ":
            return False

        banwords = ctx.bot.channels[ctx.channel.name].banwords
        for chave in banwords.keys():
            if chave in resposta:
                tamanho = len(chave)
                asteriscos = "".join("*" for _ in range(tamanho))
                resposta = resposta.replace(chave, asteriscos)

        if handle == "echo":
            if len(resposta) < 450:
                return await ctx.reply(f"{resposta}")
            parte1 = resposta[:450]
            parte2 = resposta[450:]
            await ctx.reply(f"{parte1}")
            await asyncio.sleep(0.5)
            return await ctx.reply(f"{parte2}")

        if len(resposta) < 450:
            return await ctx.reply(f"{ctx.user.nickname or ctx.author.name} {resposta}")

        resposta = f"{ctx.user.nickname or ctx.author.name} {resposta}"

        tamanho_do_chunk = 450

        chunks = []
        while len(resposta) > tamanho_do_chunk:
            # Procura o último espaço antes da posição de tamanho_do_chunk
            indice_espaco = resposta.rfind(" ", 0, tamanho_do_chunk)

            # Se não houver espaço, divide a string na posição do tamanho do chunk
            if indice_espaco == -1:
                chunks.append(resposta[:tamanho_do_chunk])
                resposta = resposta[tamanho_do_chunk:]
            else:
                # Divide a string no último espaço antes do tamanho do chunk
                chunks.append(resposta[:indice_espaco])
                resposta = resposta[indice_espaco + 1 :]

        chunks.append(resposta)

        for chunk in chunks:
            await ctx.reply(chunk)
            if len(chunks) > 5:
                await asyncio.sleep(0.5)
            elif len(chunks) > 10:
                await asyncio.sleep(1)
            else:
                await asyncio.sleep(0.12)


def check(check: list) -> Callable[[Command], Command]:
    def decorator(command: Command) -> Command:
        # if type(command) != Command:
        #     raise TypeError(f"Expected 'twitchio.ext.commands.Command', not '{type(command)}'")
        for c in check:
            command._checks.append(c)
        return command

    return decorator

#
# def usage(usage: str) -> Callable[[Command], Command]:
#     def decorator(command: Command) -> Command:
#         # if type(command) != Command:
#         #     raise TypeError(f"Expected 'twitchio.ext.commands.Command', not '{type(command)}'")
#         command.usage = usage
#         return command
#
#     return decorator
#
#
# def helper(description: str) -> Callable[[Command], Command]:
#     def decorator(command: Command) -> Command:
#         # if type(command) != Command:
#         #     raise TypeError(f"Expected 'twitchio.ext.commands.Command', not '{type(command)}'")
#         command.description = description
#         return command
#
#     return decorator
#
#
# def base_decorator(base: BaseDecorator) -> Callable[[Command], Command]:
#     def decorator(command: Command) -> Command:
#         command.decorators = base
#         return command
#
#     return decorator




























