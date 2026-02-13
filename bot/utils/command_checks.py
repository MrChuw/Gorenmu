from __future__ import annotations

import logging
from datetime import datetime

from bot.exceptions import (
    BotOfflineError,
    CommandDisabledError,
    ContentHasBanwordError,
    DevRequiredError,
    GameIsAlreadyRunningError,
    ModRequiredError,
    OwnerRequiredError,
    SubRequiredError,
    UnknownErrorError,
    UserIsNotAllowedError,
    VipRequiredError,
)
from bot.ext import Context
from bot.utils.string_manipulation import StringTools


class RoleCheck:
    @staticmethod
    def owner(ctx: Context) -> bool:
        return ctx.author.name == ctx.channel.name

    @staticmethod
    def dev(ctx: Context) -> bool:
        return int(ctx.author.id) == ctx.bot.config.BotConfig.dev_userid

    @staticmethod
    def admin(ctx: Context) -> bool:
        return RoleCheck.broadcaster(ctx) or RoleCheck.mod(ctx) or RoleCheck.owner(ctx) or RoleCheck.dev(ctx)

    @staticmethod
    def broadcaster(ctx: Context) -> bool:
        return ctx.author.broadcaster

    @staticmethod
    def lead_mod(ctx: Context) -> bool:
        return ctx.author.lead_moderator

    @staticmethod
    def mod(ctx: Context) -> bool:
        return ctx.author.moderator or RoleCheck.lead_mod(ctx)

    @staticmethod
    def vip(ctx: Context) -> bool:
        return ctx.author.vip

    @staticmethod
    def sub(ctx: Context) -> bool:
        return ctx.author.subscriber

    @staticmethod
    def sponsor(ctx: Context) -> bool:
        return bool(ctx.user and ctx.user.sponsor)


class Role:
    @staticmethod
    def owner(ctx: Context) -> bool:
        if RoleCheck.owner(ctx):
            return True
        raise OwnerRequiredError

    @staticmethod
    def dev(ctx: Context) -> bool:
        if RoleCheck.dev(ctx):
            return True
        raise DevRequiredError

    @staticmethod
    def admin(ctx: Context) -> bool:
        if RoleCheck.admin(ctx):
            return True
        raise ModRequiredError

    @staticmethod
    def vip(ctx: Context) -> bool:
        if RoleCheck.vip(ctx):
            return True
        raise VipRequiredError

    @staticmethod
    def sub(ctx: Context) -> bool:
        if RoleCheck.sub(ctx):
            return True
        raise SubRequiredError

    @staticmethod
    def sponsor(ctx: Context) -> bool:
        return RoleCheck.sponsor(ctx)

    @staticmethod
    def any(ctx: Context) -> bool:  # NOQA
        return True


class Check:
    @staticmethod
    def allowed(ctx: Context) -> bool:
        if not Role.any(ctx) and StringTools.str2url(ctx.content) is not None:
            raise UserIsNotAllowedError()
        return True

    @staticmethod
    def banword(ctx: Context) -> bool:
        if any(word in ctx.message.text for word in ctx.bot.channels[ctx.channel.name].banwords):
            raise ContentHasBanwordError()
        return True

    @staticmethod
    def enabled(ctx: Context) -> bool:
        if ctx.command.name in ctx.bot.channels[ctx.channel.name].disabled:
            raise CommandDisabledError()
        return True

    @staticmethod
    def game(ctx: Context) -> bool:
        if ctx.bot.cache.get(f"game-{ctx.channel.name}"):
            raise GameIsAlreadyRunningError()
        return True

    @staticmethod
    def online(ctx: Context) -> bool:
        if not ctx.bot.channels[ctx.channel.name].online:
            raise BotOfflineError()
        return True

    @staticmethod
    async def lottery_seed(ctx: Context) -> bool:
        from tortoise.exceptions import DoesNotExist, MultipleObjectsReturned

        from bot.models import Cookies, LotteryBank
        from bot.models import User as UserModel

        try:
            await Cookies.get(id=int(ctx.author.id))
        except DoesNotExist:
            user = await UserModel.get(id=int(ctx.author.id))
            await Cookies.create(user=user, id=int(ctx.author.id))
        except MultipleObjectsReturned as e:
            logging.error(e)
            await ctx.reply(
                ctx.component.translations.Exceptions.lottery_seed(ctx.bot.dev_user.display_name).response_string
            )
            raise UnknownErrorError from e
        if not await LotteryBank.get_or_none(closed=False, accumulated=True):
            await LotteryBank.create()
        ctx.bot.lottery_seed = datetime.now().toordinal()
        return True

    # COOKIE
    @staticmethod
    async def cookie_check(ctx: Context, translations) -> bool:
        from tortoise.exceptions import DoesNotExist

        from bot.models import Cookies

        try:
            cookie = await Cookies.get_cookie(ctx=ctx, user=ctx.user, translations=translations)
        except DoesNotExist:
            cookie = await Cookies.create(user=ctx.user, id=int(ctx.author.id))
        if hasattr(cookie, "response_string"):
            cookie = await Cookies.create(user=ctx.user, id=int(ctx.author.id))
        if not cookie.cooldown:
            await cookie.new_cooldown()
        return True

    @staticmethod
    async def interactive_check(ctx: Context) -> bool:
        if ctx.args and isinstance(ctx.args[0], str):
            ctx.args[0] = ctx.args[0].lstrip("@").rstrip(",").lower()
        if len(ctx.args) > 1 and isinstance(ctx.args[1], str):
            ctx.args[1] = ctx.args[1].lstrip("@").rstrip(",").lower()
        return True
