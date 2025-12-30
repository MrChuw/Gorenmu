from __future__ import annotations

import re
import string
from typing import TYPE_CHECKING

from bot.ext import Context, Response, commands
from bot.utils import StringTools

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class SetCmd(commands.CustomComponent):
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

    @commands.group(name="set", aliases=[], invoke_fallback=True)
    async def set(self, ctx: Context, *, args) -> Response:
        return self.translations.Exceptions.echo(ctx, args)

    @set.command(name="mention", aliases=[])
    async def set_mention(self, ctx: Context, *, args: str) -> Response:
        translations = self.translations.Mention
        if args.lower() not in ["on", "off"]:
            return translations.on_off_wrong_option(ctx, args)
        ctx.user.mention = args.lower() == "on"
        await ctx.user.save()
        return translations.mention_on(ctx) if args == "on" else translations.mention_off(ctx)

    @set.command(name="city", aliases=["savecity", "savelocation", "location"], whispable=True)
    async def set_city(self, ctx: Context, *, args: str) -> Response:
        translations = self.translations.City
        args, hidden = self.StringTools.extract_and_remove_bool_field(args, "hidden", self.translations, ctx)
        city = args.lower()
        ctx.user.city_hidden = True
        if hidden is False:
            ctx.user.city_hidden = False
        if city == "remove":
            ctx.user.city = None
            await ctx.user.save()
            return translations.city_removed(ctx)
        ctx.user.city = city
        await ctx.user.save()
        return translations.city_added(ctx)

    @set.command(name="nick", aliases=["nickname"])
    async def set_nick(self, ctx: Context, *, args: str) -> Response:
        translations = self.translations.Nick
        nickname = args
        if len(nickname) > 32:
            return translations.nick_too_large(ctx, len(nickname))
        if nickname[0] in string.punctuation:
            nickname = f"️{args}"
        if nickname.lower() == "remove":
            ctx.user.nick = None
            await ctx.user.save()
            return translations.nick_removed(ctx)
        ctx.user.nick = nickname
        await ctx.user.save()
        return translations.nick_changed(ctx)

    @set.command(name="color", aliases=[])
    async def set_color(self, ctx: Context, *, args: str) -> Response:
        translations = self.translations.Color
        if args.lower() == "remove":
            ctx.user.color = None
            await ctx.user.save()
            return translations.color_removed(ctx)
        match = re.match(r"^#?([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$", args)
        color = f"#{match[1].lower()}" if match else ctx.author.color
        ctx.user.color = color
        await ctx.user.save()
        return translations.color_changed(ctx, color)

    @set.command(name="reminder", aliases=[])
    async def set_reminder(self, ctx: Context, *, args: str) -> Response:
        translations = self.translations.Reminder
        if args.lower() not in ["on", "off"]:
            return self.translations.Mention.on_off_wrong_option(ctx, args)
        if args.lower() == "on":
            ctx.user.block = True
            await ctx.user.save()
            return translations.reminder_on(ctx)
        else:
            ctx.user.block = False
            await ctx.user.save()
            return translations.reminder_off(ctx)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(SetCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
