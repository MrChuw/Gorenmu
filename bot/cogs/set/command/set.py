from __future__ import annotations

import re
import string
from typing import TYPE_CHECKING

from bot.ext import Context, Response, commands
from bot.utils import Role, StringTools

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class SetCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot, self)
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

    @commands.group(name="set", aliases=[], invoke_fallback=True)
    async def set(self, ctx: Context, *, args) -> Response:  # NOQA
        return self.translations.Exceptions.echo(args)

    @set.command(name="mention", aliases=[], pipeble=False)
    async def set_mention(self, ctx: Context, *, args: str) -> Response:
        translations = self.translations.Mention
        if args.lower() not in ["on", "off"]:
            return translations.on_off_wrong_option(args)
        ctx.user.mention = args.lower() == "on"
        await ctx.user.save()
        return translations.mention_on() if args == "on" else translations.mention_off()

    @set.command(name="city", aliases=["savecity", "savelocation", "location"], whispable=True)
    async def set_city(self, ctx: Context, *, args: str) -> Response:
        translations = self.translations.City
        args, hidden = self.StringTools.extract_and_remove_bool_field(args, "hidden", self.translations)
        city = args.lower()
        ctx.user.city_hidden = True
        if hidden is False:
            ctx.user.city_hidden = False
        if city == "remove":
            ctx.user.city = None
            await ctx.user.save()
            return translations.city_removed()
        ctx.user.city = city
        await ctx.user.save()
        return translations.city_added()

    @set.command(name="nick", aliases=["nickname"], pipeble=False)
    async def set_nick(self, ctx: Context, *, args: str) -> Response:
        translations = self.translations.Nick
        nickname = args
        if len(nickname) > 32:
            return translations.nick_too_large(len(nickname))
        if nickname[0] in string.punctuation:
            nickname = f"️{args}"
        if nickname.lower() == "remove":
            ctx.user.nickname = None
            await ctx.user.save()
            return translations.nick_removed()
        ctx.user.nickname = nickname
        await ctx.user.save()
        return translations.nick_changed()

    @set.command(name="color", aliases=[], pipeble=False)
    async def set_color(self, ctx: Context, *, args: str) -> Response:
        translations = self.translations.Color
        if args.lower() == "remove":
            ctx.user.color = None
            await ctx.user.save()
            return translations.color_removed()
        match = re.match(r"^#?([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$", args)
        color = f"#{match[1].lower()}" if match else ctx.author.color
        ctx.user.color = color
        await ctx.user.save()
        return translations.color_changed(color)

    @set.command(name="reminder", aliases=[], pipeble=False)
    async def set_reminder(self, ctx: Context, *, args: str) -> Response:
        translations = self.translations.Reminder
        if args.lower() not in ["on", "off"]:
            return self.translations.Mention.on_off_wrong_option(args)
        if args.lower() == "on":
            ctx.user.block = True
            await ctx.user.save()
            return translations.reminder_on()
        else:
            ctx.user.block = False
            await ctx.user.save()
            return translations.reminder_off()

    @commands.guard([Role.admin])
    @set.command(name="banword", aliases=[])
    async def set_banword(self, ctx: Context, action: str, *, args: str) -> Response:
        translations = self.translations.Banword
        words = translations.add_remove_lang()
        _words = self.StringTools.extract_words_simple(args)
        add, remove, clean = words.get("add"), words.get("remove"), words.get("clean")
        channel = self.bot.channels[ctx.channel.name.lower()]
        if channel.removed:
            return translations.who()
        if action.lower() not in ["add", "remove", "clean", *clean, *add, *remove]:
            await self._send_bug(ctx, ctx.channel.name)
            return translations.add_remove(action)
        if action.lower() in ["add", *add]:
            for world in _words:
                channel.banwords[world] = int(ctx.author.id)
            await channel.save()
            return translations.added()
        elif action.lower() in ["remove", *remove]:
            for world in _words:
                channel.banwords.pop(world)
            await channel.save()
            return translations.removed()
        elif action.lower() in ["clean", *clean]:
            channel.banwords = {}
            return translations.cleaned()
        else:
            return translations.what(action)

    @commands.guard([Role.admin])
    @set.command(name="enable", aliases=["disable"], pipeble=False)
    async def set_enable_disable(self, ctx: Context, arg: str) -> Response:
        translations = self.translations.Enable
        channel = self.bot.channels[ctx.channel.name.lower()]
        invoked = ctx.invoked_with.lower()
        protected_commands = {"set", "enable", "disable", "help", "start", "stop"}
        if arg.lower() in protected_commands:
            return translations.why(arg)
        if arg.lower() == "all":
            if invoked == "set enable":
                channel.disabled.clear()
                await channel.save()
                return translations.all_enabled()
            elif invoked == "set disable":
                for cmd in ctx.bot.commands:
                    if ctx.bot.commands[cmd].name not in protected_commands:
                        channel.disabled[ctx.bot.commands[cmd].name.lower()] = int(ctx.author.id)
                await channel.save()
                return translations.all_disabled()
        command_to_manage = ctx.bot.get_command(arg.lower())
        if not command_to_manage:
            return translations.no_command(arg)
        if invoked == "set enable":
            if command_to_manage.name not in channel.disabled:
                return translations.command_already_enabled(arg)
            channel.disabled.pop(command_to_manage.name.lower(), None)
            await channel.save()
            return translations.command_enabled(arg)
        elif invoked == "set disable":
            if command_to_manage.name in protected_commands:
                return translations.why(arg)
            if command_to_manage.name in channel.disabled:
                return translations.command_already_disabled(arg)
            channel.disabled[command_to_manage.name.lower()] = int(ctx.author.id)
            await channel.save()
            return translations.command_disabled(arg)
        return translations.options()

    @commands.guard([Role.admin])
    @set.command(name="prefix", aliases=[], pipeble=False)
    async def set_prefix(self, ctx: Context, arg: str) -> Response:
        translations = self.translations.Prefix
        prefix_size = 2
        if len(arg) >= prefix_size:
            return translations.too_long(arg, prefix_size)
        channel = self.bot.channels[ctx.channel.name.lower()]
        channel.prefix = arg
        await channel.save()
        return translations.prefix_changed(arg)

    @commands.guard([Role.admin])
    @set.command(name="start", aliases=["on", "stop", "off"], pipeble=False, whispable=True)
    async def set_start_stop(self, ctx: Context) -> Response:
        translations = self.translations.StartStop
        invoked = ctx.invoked_with.lower()
        channel = self.bot.channels[ctx.channel.name.lower()]
        if invoked.lower() in ["set start", "set on"]:
            if channel.online:
                return translations.already_on()
            channel.online = True
            await channel.save()
            return translations.started()
        elif invoked.lower() in ["set stop", "set off"]:
            await channel.save()
            if channel.online:
                channel.online = False
                await channel.save()
                return translations.stopped()
            return translations.already_off()
        return translations.shrug()

    async def _send_bug(self, ctx: Context, name: str):
        if self.bot.mock:
            return None
        fake_exc = self.translations.SupportTools.fake_stacktrace(
            f"Somehow a command has invoked for removed channel: {name}"
        )
        return await self.bot.CommandHandler.send_bug(ctx, fake_exc)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(SetCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
