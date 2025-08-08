# -*- coding: utf-8 -*-
from __future__ import annotations

import re
import string
from typing import TYPE_CHECKING

from bot.ext import Context, commands
from bot.translations import Response

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class SetCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: commands.Context) -> bool:  # NOQA
        return True

    @commands.base_decorator("Set")
    @commands.group(name="set", aliases=[], invoke_fallback=True)
    async def set(self, ctx: Context, *, args) -> Response:
        translations = ctx.user.translations.Admin.Nada
        return translations.nada.format_response(ctx, args, success=True)

    @commands.base_decorator("Set.Mention")
    @set.command(name="mention", aliases=[])
    async def set_mention(self, ctx: Context, *, args: str) -> Response:
        translations = ctx.user.translations.Set
        if args.lower() not in ["on", "off"]:
            return translations.on_off_wrong_option.format_response(ctx, args, success=False)
        ctx.user.mention = args.lower() == "on"
        await ctx.user.save()
        return (
            translations.mention_on.format_response(ctx)
            if args == "on"
            else translations.mention_off.format_response(ctx)
        )

    @commands.base_decorator("Set.City")
    @set.command(name="city", aliases=["savecity", "savelocation", "location"])
    async def set_city(self, ctx: Context, *, args: str) -> Response:
        translations = ctx.user.translations.Set
        args, hidden = ctx.bot.StringTools.extract_and_remove_field(args, "hidden")
        city = args.lower()
        if hidden:
            ctx.user.city_hidden = True
        if city == "remove":
            ctx.user.city = None
            await ctx.user.save()
            return translations.city_removed.format_response(ctx)
        ctx.user.city = city
        await ctx.user.save()
        return translations.city_added.format_response(ctx)

    @commands.base_decorator("Set.Nick")
    @set.command(name="nick", aliases=["nickname"])
    async def set_nick(self, ctx: Context, *, args: str) -> Response:
        translations = ctx.user.translations.Set
        nickname = args
        if len(nickname) > 32:
            return translations.nick_too_large.format_response(ctx, len(nickname), success=False)
        if nickname[0] in string.punctuation:
            nickname = f"️{args}"
        if nickname.lower() == "remove":
            ctx.user.nick = None
            await ctx.user.save()
            return translations.nick_removed.format_response(ctx)
        ctx.user.nick = nickname
        await ctx.user.save()
        return translations.nick_changed.format_response(ctx)

    @commands.base_decorator("Set.Color")
    @set.command(name="color", aliases=[])
    async def set_color(self, ctx: Context, *, args: str) -> Response:
        translations = ctx.user.translations.Set
        if args.lower() == "remove":
            ctx.user.color = None
            await ctx.user.save()
            return translations.color_removed.format_response(ctx)
        match = re.match(r"^#?([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$", args)
        color = f"#{match[1].lower()}" if match else ctx.author.color
        ctx.user.color = color
        await ctx.user.save()
        return translations.color_changed.format_response(ctx, color)

    @commands.base_decorator("Set.Reminder")
    @set.command(name="reminder", aliases=[])
    async def set_reminder(self, ctx: Context, *, args: str) -> Response:
        translations = ctx.user.translations.Set
        if args.lower() not in ["on", "off"]:
            return translations.on_off_wrong_option.format_response(ctx, args, success=False)
        if args.lower() == "on":
            ctx.user.block = True
            await ctx.user.save()
            return translations.reminder_on.format_response(ctx)
        else:
            ctx.user.block = False
            await ctx.user.save()
            return translations.reminder_off.format_response(ctx)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(SetCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
