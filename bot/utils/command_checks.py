# -*- coding: utf-8 -*-
from __future__ import annotations

import logging
from datetime import datetime

from tortoise.exceptions import DoesNotExist, MultipleObjectsReturned

from bot.exceptions import (
    BotOffline, CommandDisabled, ContentHasBanword, DevRequired, GameIsAlreadyRunning, ModRequired, OwnerRequired,
    SubRequired, UnknownError, UserIsNotAllowed, VipRequired,
)
from bot.ext.commands import Context
from bot.models import (Cookies as CookieModel, LotteryBank, User as UserModel)
from bot.utils.string_manipulation import str2url


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
        if ctx.author.is_mod or Role.owner(ctx) or Role.dev(ctx):
            return True
        raise ModRequired

    @staticmethod
    def vip(ctx: Context) -> bool:
        if ctx.author.badges and ctx.author.badges.get("vip"):
            return True
        raise VipRequired

    @staticmethod
    def sub(ctx: Context) -> bool:
        if ctx.author.is_subscriber:
            return True
        raise SubRequired

    @staticmethod
    def sponsor(ctx: Context) -> bool:
        return ctx.user and ctx.user.sponsor

    @staticmethod
    def any(ctx: Context) -> bool:
        return (Role.sub(ctx) or Role.vip(ctx) or Role.admin(ctx) or Role.owner(ctx) or Role.dev(ctx) or Role.sponsor(
            ctx
            ))


class Check:
    @staticmethod
    def allowed(ctx: Context) -> bool:
        if not Role.any(ctx) and str2url(ctx.message.content) is not None:
            raise UserIsNotAllowed()
        return True

    @staticmethod
    def banword(ctx: Context) -> bool:
        if any(word in ctx.message.content for word in ctx.bot.channels[ctx.channel.name].banwords):
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
            await CookieModel.get(id=int(ctx.author.id))
        except DoesNotExist:
            user = await UserModel.get(id=int(ctx.author.id))
            await CookieModel.create(user=user, id=int(ctx.author.id))
        except MultipleObjectsReturned as e:
            logging.error(e)
            await ctx.reply(ctx.translations.Exceptions.LotteryExceptions().lottery_seed)
            raise UnknownError
        if not await LotteryBank.get_or_none(encerrada=False, acumulado=True):
            await LotteryBank.create()
        if ctx.bot.lottery_seed:
            ctx.bot.lottery_seed = datetime.now().toordinal()
        else:
            ctx.bot.lottery_seed = datetime.now().toordinal()
        return True

    # COOKIE: Mudar como o bônus dos cookies funciona.
    @staticmethod
    async def cookie_check(ctx: Context) -> bool:
        cookie = CookieModel.get_or_none(id=int(ctx.author.id))
        if not cookie:
            user = await UserModel.get(id=int(ctx.author.id))
            await CookieModel.create(user=user, id=int(ctx.author.id))
        ctx.bot.CookieTools.seed = datetime.now().toordinal()
        if ctx.bot.CookieTools.seed % 100 == 0:
            ctx.bot.CookieTools.multiplicador = 5
        elif ctx.bot.CookieTools.seed % 10 == 5:
            ctx.bot.CookieTools.multiplicador = 2
        return True

    @staticmethod
    async def interactive_check(ctx: Context) -> bool:
        if ctx.args and isinstance(ctx.args[0], str):
            ctx.args[0] = ctx.args[0].lstrip("@").rstrip(",").lower()
        if len(ctx.args) > 1 and isinstance(ctx.args[1], str):
            ctx.args[1] = ctx.args[1].lstrip("@").rstrip(",").lower()
        return True

    @staticmethod
    async def language_set(ctx: Context) -> bool:
        ctx.translations = ctx.bot.TranslationManager.get_translations(ctx.user.language or "pt-br")
        ctx.decorators = ctx.bot.TranslationManager.get_decorator(ctx.user.language or "pt-br")
        return True
