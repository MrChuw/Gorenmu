from __future__ import annotations

from typing import TYPE_CHECKING

from bot.apis import ApiIvrFi
from bot.ext import Context, Response, commands
from bot.utils import SessionsCaches, StringTools

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class FollowAgeCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot, self)
        self.StringTools: StringTools = StringTools()
        self.SessionsCaches: SessionsCaches = SessionsCaches(bot)
        self.ApiIvrFi: ApiIvrFi = ApiIvrFi(bot, self.SessionsCaches.IvrFi.session)

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    async def component_before_invoke(self, ctx: Context) -> None:
        self.translations.ctx_set(ctx)

    @commands.Component.guard()
    def guards_component(self, ctx: commands.Context) -> bool:  # NOQA
        return True

    @commands.command(name="followage", aliases=[])
    async def followage(self, ctx: Context, name: str, channel: str = "") -> Response:
        name = self.StringTools.str2name(name)
        channel = self.StringTools.str2name(channel or ctx.channel.name)

        if name == channel:
            return self.translations.FollowAge.self_follow()

        user = await ctx.bot.fetch_user(login=name, token_for=self.bot.user)
        if not user:
            return self.translations.Exceptions.user_not_found_name(name)

        broadcaster = await ctx.bot.fetch_user(login=channel)
        if not broadcaster:
            return self.translations.Exceptions.user_not_found_name(channel)

        mention = self.translations.SupportTools.LanguageContext.mention(name, ctx.author.name)
        mention_channel = self.translations.SupportTools.LanguageContext.mention(broadcaster.name, ctx.author.name)

        follow = await self.ApiIvrFi.Twitch.Channel.fetch_followage(channel, user.name)
        if not follow.followed_at:
            return self.translations.FollowAge.not_followed(mention, channel)
        humanize = self.translations.SupportTools.TimeTools.Humanize(ctx.user.language)
        delta = humanize.precisedelta(follow.followed_at.replace(tzinfo=None))

        return self.translations.FollowAge.follow(mention, mention_channel, delta)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(FollowAgeCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
