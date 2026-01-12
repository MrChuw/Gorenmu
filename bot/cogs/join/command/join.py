from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Context, Response, commands
from bot.models import Channel
from bot.utils import StringTools

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class JoinCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot)
        self.StringTools: StringTools = StringTools()

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: commands.Context) -> bool:  # NOQA
        return True

    async def component_before_invoke(self, ctx: Context) -> None:
        self.translations.ctx_set(ctx)

    # TODO: add more scopes later, fix get_or_none to user_id
    # TODO: also add explanations for scopes
    @commands.command(name='join', aliases=[], whispable=True)
    async def join(self, ctx: Context, args: str = "") -> Response:
        channel = await Channel.get_or_none(user_id=ctx.user.id)
        args, lang = self.StringTools.remove_prefixed_option(args, "lang")
        if channel and not channel.removed:
            channel.online = True
            channel.language = lang
            await channel.save()
            await self.bot.ChannelHandler.load_channels()
            return self.translations.Join.already_in_chat(channel.prefix)

        return self.translations.Join.website(["channel:bot"])


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(JoinCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
