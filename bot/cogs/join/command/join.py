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
        self.translations: Translations = Translations(bot, self)
        self.StringTools: StringTools = StringTools()

    # TODO: add more scopes later
    # TODO: also add explanations for scopes
    @commands.command(name='join', aliases=[], whispable=True)
    async def join(self, ctx: Context, args: str = "") -> Response:
        channel = await Channel.get_or_none(user_id=ctx.user.id)
        args, lang = self.StringTools.remove_prefixed_option(args, "lang")
        if channel and not channel.removed:
            channel.online = True
            channel.language = lang  # type: ignore[assignment]
            await channel.save()
            await self.bot.ChannelHandler.load_channels()
            return self.translations.Join.already_in_chat(channel.prefix)

        return self.translations.Join.website(["channel:bot"])


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(JoinCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
