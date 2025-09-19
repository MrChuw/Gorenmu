# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Context, Response, commands
from bot.models import Bug
from bot.utils import DiscordWebHook, SessionsCaches

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class BugCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot)
        self.SessionsCaches: SessionsCaches = SessionsCaches(bot)
        self.DiscordWebHook: DiscordWebHook = DiscordWebHook()

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: commands.Context) -> bool:  # NOQA
        return True

    @commands.command(name="bug", aliases=[])
    async def bug(self, ctx: Context, *, content) -> Response:
        session = self.SessionsCaches.Bug.session
        url = self.bot.config.Discord.bug_webhook
        display_name = ctx.author.display_name
        title = f"Bug reported by {display_name}"
        author_url = f"https://twitch.tv/{ctx.author.name}"
        await self.DiscordWebHook.send_discord_webhook(session, url, ctx, content, title, author_url)
        bug = await Bug.create(user=ctx.user, content=content)
        return self.translations.Bug.bug(ctx, bug.id)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(BugCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
