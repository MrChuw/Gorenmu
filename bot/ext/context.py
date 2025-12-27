from __future__ import annotations

from typing import TYPE_CHECKING

import twitchio
from twitchio.ext.commands import Context as TwitchioContext

if TYPE_CHECKING:
    from twitchio import ChatMessage, ChatMessageReply

    from bot.bot import Gorenmu
    from bot.ext import Command, Response
    from bot.ext.commands import CustomComponent
    from bot.models import User as UserModel


class Context(TwitchioContext):
    user: UserModel
    bot: Gorenmu
    command: Command
    component: CustomComponent
    _command: Command
    invoke_by: str | None = None
    reply_to: ChatMessageReply | None = None

    def __init__(self, message: ChatMessage, *, bot: Gorenmu, prefix: str, invoke_by: str | None):
        super().__init__(message, bot=bot)
        self._prefix: str | None = prefix
        self.invoke_by: str | None = invoke_by
        if isinstance(self._payload, twitchio.Whisper):
            self.reply_to: None = None
        else:
            self.reply_to: ChatMessageReply = message.reply

    @property
    def passed_guards(self) -> bool:
        return self._passed_guards

    def get_command(self):
        self._get_command()

    async def simple_response(self, ctx: Context, response: str, handle: str | None = None) -> None | bool:
        if ctx.bot.channels[ctx.channel.name].online is False:
            return False
        response_str = response
        response_str, user_handler = await self.bot.ContextHandler.handle_banwords(ctx, response_str)

        if handle == "echo":
            return await self.bot.ContextHandler.handle_echo(ctx=ctx, response_str=response_str)
        return await self.bot.ContextHandler.send_response(ctx, user_handler, response_str)

    async def invoke(self) -> Response | bool:
        return await self.bot.ContextHandler.invoke(self)

    @property
    def message(self) -> ChatMessage | None:
        """Property returning the :class:`~twitchio.ChatMessage` that this :class:`~.commands.Context` was
        created from. This could be ``None`` if :attr:`~.commands.Context.type` is :attr:`~.commands.ContextType.REWARD`
        """
        return self._payload  # if isinstance(self._payload, ChatMessage) else None
