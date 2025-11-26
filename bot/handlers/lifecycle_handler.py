from __future__ import annotations

import asyncio
import contextlib
from typing import TYPE_CHECKING

import twitchio

from bot.exceptions import InvalidArgument
from bot.ext import ChatMessage, Context
from bot.models import User as UserModel
from bot.models.user_extras import BotsIgnore
from bot.utils import Check, MarkovProcessor, SessionsCaches

if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.ext import Response
    from bot.utils import Config


class LifecycleHandler:
    def __init__(self, bot: Gorenmu):
        self.bot = bot
        self.config: Config = bot.config
        self.SessionsCaches: SessionsCaches = SessionsCaches(bot)

    async def setup(self):
        bot_list = await BotsIgnore.filter(active=True).all()
        self.bot.bots_ids = [bot_id.user_id for bot_id in bot_list]
        self.bot.MarkovProcessor = MarkovProcessor(self.bot)
        await self.bot.ChannelHandler.load_channels()
        self.bot.MarkovTask = asyncio.create_task(self.bot.MarkovProcessor.process_message(), name="process_message")
        await self.bot.CommandHandler.load_cogs()
        # if self.config.ApisConfig.enable_site_endpoints:
        #     asyncio.create_task(self.bot.api_start(self.bot))

    async def close(self):
        await self.bot.DatabaseHandler.close_db()
        await self.SessionsCaches.close_all_sessions()
        await self.bot.memcache.close_all_caches()
        self.bot.CommandHandler.stop_routines()
        self.bot.MarkovTask.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await self.bot.MarkovTask
        if not self.bot.mock:
            await super(type(self.bot), self.bot).close()

    async def event_ready(self):
        if not self.bot.mock:
            await self.bot.TokensHandler.setup_conduit()
        self.bot.dev_name = (await self.bot.fetch_users(ids=[self.config.BotConfig.dev_userid]))[0].display_name
        self.config.BotConfig.dev_name = self.bot.dev_name

        self.bot.log.info(
            f"{self.bot.bot_id} | {len(self.bot.channels)} Channels | "
            f"{len(self.bot._get_prefix)} prefix's, {len(self.bot.commands)} commands."  # NOQA
        )
        self.bot.bot_nick = (await self.bot.fetch_users(ids=[self.bot.bot_id]))[0].display_name
        await UserModel.get_or_create(id=self.bot.bot_id, name=self.bot.bot_nick)

    async def event_message(self, payload: ChatMessage):
        if payload.chatter.id == str(self.bot.bot_id) or payload.source_broadcaster is not None:
            return None
        ctx: Context = await self.get_context(payload)
        ctx.user, is_online = await asyncio.gather(
            UserModel.create_or_update(ctx), self.bot.ChannelHandler.is_online(payload)
        )
        if not is_online:
            return None

        ctx.message.text = ctx.message.text.replace("\U000e0000", "")
        if not ctx.command:
            await self.bot.MarkovProcessor.put_markov_queue(ctx)

        try:
            channel = self.bot.channels[payload.broadcaster.name]
            if not channel.online and "start" not in payload.text:
                return None
            response: Response | None = None
            if ctx.command:
                self.bot.log.info(f"#{ctx.channel.name}|| @{ctx.author.name}: {ctx.message.text}")

                has_double_prefix = f"{ctx.prefix}{ctx.prefix}" in ctx.message.text
                message_has_pipe = " | " in ctx.message.text
                is_alias_command = f"{ctx.prefix}alias" in ctx.message.text
                if has_double_prefix:
                    response = await self.bot.ContextHandler.alias_handler(ctx, payload)
                elif message_has_pipe and not is_alias_command:
                    await self.bot.ContextHandler.pipe_handler(ctx, payload)
                else:
                    response = await ctx.invoke()
                if response:
                    await self.bot.ContextHandler.response(response)
            await self.manual_event_message(ctx)
            return None

        except InvalidArgument:
            deco = ctx.command.component.translations.get_decorator(ctx=ctx)
            if usage := deco.deco_usage(ctx):
                return await ctx.reply(usage)

            error_not_registered = ctx.command.component.translations.Exceptions.error_not_registered(
                ctx, self.config.BotConfig.dev_name
            )
            return await ctx.simple_response(ctx, error_not_registered.response_string)
        except Exception as error:
            self.bot.log.error(error)
            return False

    async def event_message_whisper(self, payload: twitchio.Whisper):  # TODO: TODO
        ...

    async def _handle_events(self, event_name: str, ctx: Context):
        for category in self.bot.manual_events:
            events = self.bot.manual_events[category]
            if event_name not in events:
                return
            for name, func in events[event_name].items():
                try:
                    response = await func(ctx)
                    if not response:
                        continue
                    elif isinstance(response, Response):
                        await self.bot.ContextHandler.response(response)
                    elif isinstance(response, str):
                        await self.bot.ContextHandler.simple_response(ctx, response)
                except Exception as e:
                    self.bot.log.error(f"Error handling event {event_name} func name {name}: {e}")

    async def manual_event_message(self, ctx: Context):
        if not ctx.user:
            ctx.user = await UserModel.create_or_update(ctx)
        await self._handle_events("event_message", ctx)

    async def event_command_invoked(self, ctx: Context):
        await self._handle_events("command_invoked", ctx)

    async def event_command_completed(self, ctx: Context):
        await self._handle_events("command_completed", ctx)

    async def before_invoke(self, ctx: Context):
        await self._handle_events("before_invoke", ctx)

    async def after_invoke(self, ctx: Context):
        await self._handle_events("after_invoke", ctx)

    @staticmethod
    async def global_guard(ctx: Context) -> bool:
        checks = [Check.online, Check.enabled]
        return all(check(ctx) for check in checks)

    async def get_prefix(self, message: ChatMessage):
        if message.subscription_type == "user.whisper.message":
            return "+"
        return self.bot.channels[message.broadcaster.name].prefix

    async def get_context(self, payload: ChatMessage | twitchio.Whisper) -> Context:
        if "\x01ACTION " in payload.text:
            payload.text = payload.text.replace("\x01ACTION ", "").replace("\x01", "")
        invoke_by = None
        if payload.reply:
            payload.text = payload.text.removeprefix(payload.reply.parent_user.mention).lstrip()
            payload.text = f"{payload.text} {payload.reply.parent_message_body}"

        prefix = await self.get_prefix(payload)
        prefix_in = prefix in payload.text
        if payload and payload.text and prefix_in:
            invoke_by = payload.text.partition(" ")[0][len(prefix) :].lower()

        ctx = Context(
            message=payload,
            bot=self.bot,
            prefix=prefix if prefix_in else None,
            invoke_by=invoke_by,
        )
        ctx.get_command()
        return ctx
