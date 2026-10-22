from __future__ import annotations

from typing import TYPE_CHECKING

from bot.apis.best_logs import BestLogs
from bot.ext import Context, Response, commands
from bot.utils import SessionsCaches, StringTools

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class UserIdCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot, self)
        self.SessionsCaches: SessionsCaches = SessionsCaches(bot)
        self.StringTools: StringTools = StringTools()
        self.BestLogs: BestLogs = BestLogs(bot, self.SessionsCaches.UserId.session)

    # TODO: Make twitch gql shit later with invoke by u
    @commands.command(name='userid', aliases=["u"])
    async def userid(self, ctx: Context, user_input: str | None = None) -> Response:
        reply = ctx.get_reply
        if not user_input and not reply:
            user_input = user_input or ctx.author_name
        if reply:
            user_input = reply.parent_user.name or ctx.author_name
        user_input = user_input or ctx.author_name
        try:
            if user_input.isdigit():
                user = await ctx.bot.fetch_user(id=int(user_input))
                if not user:
                    return self.translations.Exceptions.user_not_found_id(str(user_input))
                return self.translations.UserId.id_or_name(user.display_name)
            else:
                user = await ctx.bot.fetch_user(login=user_input)
                if not user:
                    return self.translations.Exceptions.user_not_found_name(str(user_input))
                return self.translations.UserId.id_or_name(user.id)
        except Exception as e:
            await self.bot.CommandHandler.send_bug(ctx, e, ping=False)
            if user_input.isdigit():
                return self.translations.UserId.unknown_id(user_input)
            else:
                return self.translations.UserId.unknown_name(user_input)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(UserIdCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
