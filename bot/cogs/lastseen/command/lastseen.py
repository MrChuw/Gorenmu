from __future__ import annotations

import datetime
import random
from typing import TYPE_CHECKING

from bot.ext import Context, Response, commands
from bot.models import User
from bot.utils import StringTools

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class LastSeenCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot, self)
        self.StringTools: StringTools = StringTools()

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    async def component_before_invoke(self, ctx: Context) -> None:
        self.translations.ctx_set(ctx)

    @commands.Component.guard()
    def guards_component(self, ctx: commands.Context) -> bool:  # NOQA
        return True

    @commands.command(name="lastseen", aliases=["ls"])
    async def lastseen(self, ctx: Context, *, args="") -> Response:
        if not args:
            args = ctx.channel.name
        name = self.StringTools.str2name(args)
        if name == ctx.bot.bot_user.display_name.lower():
            return self.translations.LastSeen.bot()
        elif name == ctx.author.name.lower():
            return self.translations.LastSeen.author()
        elif not (user := await User.get_or_none(name=name)):
            return self.translations.Exceptions.user_not_found_name(name)
        elif not user.mention:
            offset = random.randint(10, 61)
            offset = user.updated_at - datetime.timedelta(minutes=offset)
            time = self.translations.SupportTools.TimeTools.Humanize(ctx.user.language).naturaltime(offset)
            return self.translations.LastSeen.not_authorized(name + self.StringTools.inv_char(), time)
        else:
            time = self.translations.SupportTools.TimeTools.Humanize(ctx.user.language).updated_a_time(user.updated_at)
            return self.translations.LastSeen.last_seen(name, user.channel, user.content, time)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(LastSeenCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
