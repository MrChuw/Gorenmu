from __future__ import annotations

import asyncio
import importlib.util
import os
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

from bot.ext import Context, Response, commands
from bot.utils import Role, SessionsCaches, StringTools
from bot.utils.singleton import Singleton

from .translations import Translations

# from bot.models import User as UserBot
# import asyncio
# import asyncmy
# from asyncmy.cursors import DictCursor

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class AdminSmallCmds(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot)
        self.SessionsCaches: SessionsCaches = SessionsCaches(bot)
        self.StringTools: StringTools = StringTools()

    name = "Admin Commands"
    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    async def component_before_invoke(self, ctx: Context) -> None:
        self.translations.ctx_set(ctx)

    @commands.Component.guard()
    def is_dev(self, ctx: Context) -> bool:
        return Role.dev(ctx)

    @commands.command(name="nada", aliases=[])
    async def nada(self, ctx: Context, *, args: str = "") -> Response:  # NOQA
        # if " " in args:
        #     command, subcommand = args.split()
        #     command = ctx.bot.get_command(command)
        #     try:
        #         command = command.get_command(subcommand)
        #     except Exception as e:
        #         print(e)
        #
        #     teste = command.component.translations.get_decorator(ctx=command)
        #     teste2 = teste.deco_usage(ctx, prefix=ctx.prefix)
        #     await ctx.reply(teste2)
        # channel = self.bot.channels[ctx.channel.name.lower()]
        # channel = await ChannelBot.get(user_id=192923262)
        # markov = await self.bot.MarkovProcessor.generate(args, channel=channel, max_length=25)
        # await self.bot.ContextHandler.simple_response(ctx, str(self.bot.MarkovProcessor.queue.async_q.qsize()))

        return self.translations.Nada.nada(args + self.StringTools.inv_char())
        # return self.translations.Exceptions.echo(ctx, markov)

    # @commands.command(name="nada2", aliases=[])
    # async def nada2(self, ctx: Context, *, args: str) -> Response:
    #     channel = self.bot.channels[ctx.channel.name.lower()]
    #     user = ctx.user
    #     rows = await fetch_message_logs(ctx)
    #     # with open("texts.txt") as text:
    #     #     mensagens = text.readlines()
    #     # for msg in mensagens:
    #     #     await self.bot.MarkovProcessor.queue.async_q.put((msg, channel, user))
    #     for row in rows:
    #         try:
    #             user, success = await UserBot.get_or_create(id=row["user"].id, name=row["user"].name)
    #             if row['channel'].id not in [411010313, 926706091, 707980467, 54966942, 744028864, ]:
    #                 channel, success = await ChannelBot.get_or_create(user_id=row['channel'].id)
    #                 if channel not in self.bot.channels and not channel.removed:
    #                     channel.removed = True
    #                     await channel.save()
    #             else:
    #                 channel = await ChannelBot.get(user_id=row['channel'].id)
    #
    #             await self.bot.MarkovProcessor.queue.async_q.put((row['message_row'].content, channel, user))
    #         except Exception as e:
    #             print(e)
    #     markov = await self.bot.MarkovProcessor.generate(args, channel=channel)
    #     return self.translations.Exceptions.echo(ctx, markov)

    @commands.command(name="restart", aliases=[])
    async def restart(self, ctx: Context) -> Response:  # NOQA
        if venv_python := os.getenv("VIRTUAL_ENV"):
            python_executable = os.path.join(venv_python, "bin", "python")
        else:
            python_executable = sys.executable
        try:
            os.execv(python_executable, [python_executable, *sys.argv])
        except Exception as e:
            self.bot.log.error(e)
            return self.translations.Restart.unexpected_error(e)

    @commands.command(name="reload", aliases=[])
    async def reload(self, ctx: Context, command: str, *, extras=False) -> Response:
        translations = self.translations.Reload

        reloader_map = {
            "tokens_handler": {
                "attr": "TokensHandler",
                "module": "bot.handlers.tokens_handler",
                "class": "TokensHandler",
                "args": [self.bot],
            },
            "channel_handler": {
                "attr": "ChannelHandler",
                "module": "bot.handlers.channel_handler",
                "class": "ChannelHandler",
                "args": [self.bot],
            },
            "lifecycle_handler": {
                "attr": "LifecycleHandler",
                "module": "bot.handlers.lifecycle_handler",
                "class": "LifecycleHandler",
                "args": [self.bot],
            },
            "command_handler": {
                "attr": "CommandHandler",
                "module": "bot.handlers.command_handler",
                "class": "CommandHandler",
                "args": [self.bot],
            },
            "context_handler": {
                "attr": "ContextHandler",
                "module": "bot.handlers.context_handler",
                "class": "ContextHandler",
                "args": [self.bot],
            },
            "markov_handler": {
                "attr": "MarkovProcessor",
                "module": "bot.utils.markov_tools",
                "class": "MarkovProcessor",
                "args": [self.bot],
            },
        }

        if command == "commands":
            await ctx.bot.CommandHandler.reload_cogs()
            return translations.commands_reloaded()

        if command == "all":
            Singleton.clear()
            results = []
            for key in ["translations", "commands", *reloader_map]:
                fake_ctx = await self.reload._callback(self, ctx, command=key)  # NOQA
                results.append(fake_ctx.response_string)
            return self.translations.Exceptions.echo(" ".join(results))

        if command in reloader_map:
            config = reloader_map[command]
            try:
                await reload_component(
                    self.bot,
                    attr_name=config["attr"],
                    module_name=config["module"],
                    class_name=config["class"],
                    args=config.get("args", []),
                )
                return translations.module_reloaded(config["attr"])
            except Exception as e:
                ctx.bot.log.error(e)
                return translations.module_reloaded_error(config["attr"], e)

        if command == "translations":
            from bot.utils.reload_util import (
                reload_all_translations,
                reload_and_get_authorized,
            )

            force = bool(extras)
            try:
                new_base = await reload_and_get_authorized("bot.ext.translations", "TranslationBase", force)
                new_cls = await reload_all_translations("Translations", force)
                for cls in new_cls:
                    cls.__bases__ = (new_base,)
                await ctx.bot.CommandHandler.reload_cogs()
                return translations.module_reloaded("Translations")
            except Exception as e:
                ctx.bot.log.error(e)
                return translations.module_reloaded_error("Translations", e)

        command_to_reload = ctx.bot.get_command(command)
        if not command_to_reload:
            return translations.command_not_found(command)

        try:
            spec = importlib.util.find_spec(command_to_reload.module)
            await ctx.bot.CommandHandler.load_command_module(Path(spec.origin).parent)
            return translations.command_reloaded(command)
        except Exception as e:
            ctx.bot.log.error(e)
            return translations.command_reloaded_error(command, e)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(AdminSmallCmds(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA


@dataclass
class User:
    id: int
    name: str


@dataclass
class Channel:
    id: int


@dataclass
class MessageLog:
    id: int
    content: str
    type: str
    created_at: datetime
    channel_id: int | None
    user_id: int


async def reload_component(bot_obj, attr_name: str, module_name: str, class_name: str, args: list | None = None):
    from bot.utils.reload_util import reload_and_get_authorized

    try:
        new_class = await reload_and_get_authorized(module_name, class_name)
        instance = new_class(*args) if args else new_class()
        old_instance = getattr(bot_obj, attr_name)
        if close_attr := getattr(old_instance, "close", None):
            if asyncio.iscoroutinefunction(close_attr):
                if old_instance.__class__.__name__ != "LifecycleHandler":
                    await close_attr()
            else:
                close_attr()
        if teardown_attr := getattr(old_instance, "teardown", None):
            await teardown_attr()
        setattr(bot_obj, attr_name, instance)
        if start_attr := getattr(instance, "setup", None):
            await start_attr()
        bot_obj.log.info(f"Reloaded {attr_name} from {module_name}.{class_name}")
    except Exception as e:
        bot_obj.log.error(f"Error reloading {attr_name}: {e}")
        raise


#
# async def fetch_message_logs(ctx: Context):
#     connection_config = {
#         "host": "127.0.0.1",
#         "port": 12398,
#         "user": ctx.bot.config.DatabaseConfig.login,
#         "password": ctx.bot.config.DatabaseConfig.password,
#         "database": ctx.bot.config.DatabaseConfig.database_uri,
#     }
#     conn = await asyncmy.connect(**connection_config)  # NOQA
#     try:
#         async with conn.cursor(DictCursor) as cursor:
#             query = """
#                 SELECT
#                     m.id AS m_id, m.content, m.type, m.created_at, m.channel_id, m.user_id,
#                     u.id AS u_id, u.name AS u_name,
#                     c.id AS c_id
#                 FROM mensage_logs m
#                 INNER JOIN user u ON m.user_id = u.id
#                 LEFT JOIN channel c ON m.channel_id = c.id
#                 ORDER BY m.id DESC
#                 LIMIT 100000;
#                 """
#
#             await cursor.execute(query)
#             results = await cursor.fetchall()
#
#             rows = []
#             for r in results:
#                 user_obj = User(id=r["u_id"], name=r["u_name"])
#                 channel_obj = Channel(id=r["c_id"]) if r["c_id"] else None
#                 msg_obj = MessageLog(
#                     id=r["m_id"],
#                     content=r["content"],
#                     type=r["type"],
#                     created_at=r["created_at"],
#                     channel_id=r["channel_id"],
#                     user_id=r["user_id"],
#                 )
#                 rows.append({"message_row": msg_obj, "user": user_obj, "channel": channel_obj})
#             return rows
#
#     finally:
#         await conn.ensure_closed()
#
