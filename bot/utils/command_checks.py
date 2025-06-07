# -*- coding: utf-8 -*-
from __future__ import annotations

import logging
from datetime import datetime

from tortoise.exceptions import DoesNotExist, MultipleObjectsReturned

from bot.exceptions import (
    BotOffline,
    CommandDisabled,
    ContentHasBanword,
    DevRequired,
    GameIsAlreadyRunning,
    ModRequired,
    OwnerRequired,
    SubRequired,
    UnknownError,
    UserIsNotAllowed,
    VipRequired,
)
from bot.ext import Context
from bot.models import Cookies, LotteryBank, User as UserModel
from bot.translations import Response
from bot.utils.string_manipulation import StringTools


class Role:
    @staticmethod
    def dev(ctx: Context) -> bool:
        if int(ctx.author.id) == ctx.bot.config.BotConfig.dev_userid:
            return True
        raise DevRequired

    @staticmethod
    def owner(ctx: Context) -> bool:
        if ctx.author.name == ctx.channel.name:
            return True
        raise OwnerRequired

    @staticmethod
    def admin(ctx: Context) -> bool:
        if ctx.author.moderator or Role.owner(ctx) or Role.dev(ctx):
            return True
        raise ModRequired

    @staticmethod
    def vip(ctx: Context) -> bool:
        if ctx.author.vip:
            return True
        raise VipRequired

    @staticmethod
    def sub(ctx: Context) -> bool:
        if ctx.author.subscriber:
            return True
        raise SubRequired

    @staticmethod
    def sponsor(ctx: Context) -> bool:
        return ctx.user and ctx.user.sponsor

    @staticmethod
    def any(ctx: Context) -> bool:  # NOQA
        return True


class Check:
    @staticmethod
    def allowed(ctx: Context) -> bool:
        if not Role.any(ctx) and StringTools.str2url(ctx.content) is not None:
            raise UserIsNotAllowed()
        return True

    @staticmethod
    def banword(ctx: Context) -> bool:
        if any(word in ctx.message.text for word in ctx.bot.channels[ctx.channel.name].banwords):
            raise ContentHasBanword()
        return True

    @staticmethod
    def enabled(ctx: Context) -> bool:
        if ctx.command.name in ctx.bot.channels[ctx.channel.name].disabled:
            raise CommandDisabled()
        return True

    @staticmethod
    def game(ctx: Context) -> bool:
        if ctx.bot.cache.get(f"game-{ctx.channel.name}"):
            raise GameIsAlreadyRunning()
        return True

    @staticmethod
    def online(ctx: Context) -> bool:
        if not ctx.bot.channels[ctx.channel.name].online:
            raise BotOffline()
        return True

    @staticmethod
    async def lottery_seed(ctx: Context) -> bool:
        try:
            await Cookies.get(id=int(ctx.author.id))
        except DoesNotExist:
            user = await UserModel.get(id=int(ctx.author.id))
            await Cookies.create(user=user, id=int(ctx.author.id))
        except MultipleObjectsReturned as e:
            logging.error(e)
            await ctx.reply(ctx.user.translations.Exceptions.lottery_seed.format(ctx.bot.dev_name))
            raise UnknownError from e
        if not await LotteryBank.get_or_none(closed=False, accumulated=True):
            await LotteryBank.create()
        ctx.bot.lottery_seed = datetime.now().toordinal()
        return True

    # COOKIE
    @staticmethod
    async def cookie_check(ctx: Context) -> bool:
        try:
            cookie = await Cookies.get_cookie(ctx=ctx, user=ctx.user)
        except DoesNotExist:
            cookie = await Cookies.create(user=ctx.user, id=int(ctx.author.id))
        if isinstance(cookie, Response):
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
