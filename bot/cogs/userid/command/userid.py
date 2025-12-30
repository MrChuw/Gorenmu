from __future__ import annotations

from typing import TYPE_CHECKING

from twitchio import ChatMessageReply

from bot.apis.best_logs import BestLogs
from bot.ext import Context, Response, commands
from bot.utils import SessionsCaches, StringTools

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class UserIdCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot)
        self.SessionsCaches: SessionsCaches = SessionsCaches(bot)
        self.StringTools: StringTools = StringTools()
        self.BestLogs: BestLogs = BestLogs(bot, self.SessionsCaches.UserId.session)

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: commands.Context) -> bool:  # NOQA
        return True

    # TODO: Make twitch gql shit later with invoke by u
    @commands.command(name='userid', aliases=["u"])
    async def userid(self, ctx: Context, user: str | None = None) -> Response:
        if isinstance(ctx.reply_to, ChatMessageReply):
            user = ctx.message.reply.parent_user.name
        user = user or ctx.author.name
        user_name = user
        try:
            if user.isdigit():
                user = await ctx.bot.fetch_user(id=int(user))
                if not user:
                    return self.translations.Exceptions.user_not_found_id(ctx, user_name)
                return self.translations.UserId.id_or_name(ctx, user.display_name)
            else:
                user = await ctx.bot.fetch_user(login=user)
                if not user:
                    return self.translations.Exceptions.user_not_found_name(ctx, user_name)
                return self.translations.UserId.id_or_name(ctx, user.id)
        except Exception as e:
            await self.bot.CommandHandler.send_bug(ctx, e, ping=False)
            if user.isdigit():
                return self.translations.UserId.unknown_id(ctx, user)
            else:
                return self.translations.UserId.unknown_name(ctx, user)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(UserIdCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
