from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Context, Response, commands
from bot.models import Suggest
from bot.utils import DiscordWebHook, SessionsCaches

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class SuggestCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot, self)
        self.SessionsCaches: SessionsCaches = SessionsCaches(bot)
        self.DiscordWebHook: DiscordWebHook = DiscordWebHook()

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    async def component_before_invoke(self, ctx: Context) -> None:
        self.translations.ctx_set(ctx)

    @commands.Component.guard()
    def guards_component(self, ctx: commands.Context) -> bool:  # NOQA
        return True

    @commands.command(name="suggest", aliases=["suggestion"])
    async def suggest(self, ctx: Context, *, content) -> Response:
        session = self.SessionsCaches.Suggest.session
        url = self.bot.config.Discord.suggest_webhook
        display_name = ctx.author.display_name
        title = f"Suggestion reported by {display_name}"
        author_url = f"https://twitch.tv/{ctx.author.name}"
        await self.DiscordWebHook.send_discord_webhook(session, url, ctx, content, title, author_url)
        bug = await Suggest.create(user=ctx.user, content=content)
        return self.translations.Suggest.suggest(bug.id)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(SuggestCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
