from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Context, Response, commands
from bot.models import Channel, TwitchTokens

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class LeaveCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot)

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: commands.Context) -> bool:  # NOQA
        return True

    async def component_before_invoke(self, ctx: Context) -> None:
        self.translations.ctx_set(ctx)

    @commands.command(name="leave", aliases=[])
    async def leave(self, ctx: Context) -> Response:
        if not (channel := await Channel.get_or_none(user=ctx.user)):
            return self.translations.Leave.not_on_channel()
        if channel.removed:
            return self.translations.Leave.not_on_channel()
        await self.bot.TokensHandler.get_event_sub_subscriptions()
        user_token = await TwitchTokens.get(user=ctx.user)
        user_token.token = None
        user_token.refresh = None
        user_token.removed = True
        await user_token.save()
        channel.removed = True
        channel.online = False
        await channel.save()
        for sub in channel.event_subs:
            await self.bot.delete_eventsub_subscription(sub)
        await self.bot.ChannelHandler.load_channels()
        return self.translations.Leave.channel_removed(ctx.author.name)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(LeaveCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
