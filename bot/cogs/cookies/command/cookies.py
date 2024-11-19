# -*- coding: utf-8 -*-
import asyncio
import datetime
from bot.bot import Gorenmu
from bot.models import User, Channel, Cookies
from bot.utils import Check, Role
from typing import Dict, Any, List, Tuple, Optional, Coroutine, Callable
from bot.ext.commands import Bucket, check, Context, cooldown, base_decorator, helper, usage, command
from bot.translations import  BaseDecorators, Response
from bot.bot import Gorenmu
from bot.ext.commands import Command
from itertools import chain, repeat
import random


@base_decorator(BaseDecorators.Cookies)
@cooldown(rate=3, per=10, bucket=Bucket.user)
@check([Check.cookie_check])
@command(name='cookies', aliases=['sm', 'cookie', 'cc'])
async def command(ctx: Context, option: str = None, *args) -> Response:
    translations = ctx.translations.Cookies
    # if ctx.invoke_by in ["cookies"] and option != "eat":
    #     return await eat(ctx, option or (1,))
    if ctx.invoke_by in ["cc"] and option != "count":
        return await cookie_count(ctx, option or (ctx.author.name,))

    elif option == "eat":
        return await eat(ctx, args)
    elif option == "count":
        return await cookie_count(ctx, args)
    elif option == "gift":
        return await gift(ctx, args)
    elif option == "stock":
        return await stock(ctx, args)
    elif option == "top":
        return await top(ctx, args)


    else:
        return translations.invalid_option.format_response(ctx)



async def calculate_cooldown(cookie: Cookies):
    if not cookie.cooldown:
        cookie.cooldown = datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=8, seconds=10)
        await cookie.save()
    return datetime.datetime.now(datetime.UTC) - cookie.cooldown


async def eat(ctx: Context, args: tuple):
    translations = ctx.translations.Cookies
    amount, *rest = chain(args, repeat(None, 1))
    cookie = await Cookies.get(user=ctx.user)
    amount = 1 if not amount or amount and not amount.isdigit() else int(amount)
    cookie_cooldown = await calculate_cooldown(cookie)
    if amount == 0:
        return translations.not_eat.format_response(ctx, success=False)
    elif amount < 0:
        return translations.negative_eat.format_response(ctx, amount, success=False)
    elif datetime.datetime.now(datetime.UTC) > cookie.cooldown:
        await cookie.daily_update(1)
        choice = random.choice(ctx.translations.Cookies.cookie_file())
        return translations.eat.format_response(ctx, choice)
    else:
        time = ctx.translations.SupportTools.Humanize.precisedelta(cookie_cooldown)
        return translations.daily_limit_reached.format_response(ctx, time, success=False)


async def cookie_count(ctx: Context, args: tuple):
    translations = ctx.translations.Cookies
    name, *rest = chain(args, repeat(None, 1))
    cookie: Cookies | None = None
    name = ctx.bot.StringTools.str2name(name) or ctx.author.name

    mention = ctx.translations.SupportTools.mention if name == ctx.author.name else f"@{name}"
    if name == ctx.bot.nick:
        return translations.cc_bot_nick.format_response(ctx, success=False)
    elif name == ctx.author.name:
        cookie = await Cookies.get_or_none(user=ctx.user)
        return translations.format_cookie_count(ctx, mention=mention, cookie=cookie)

    elif not (user := await User.get_or_none(name=name)):
        return translations.user_not_found.format_response(ctx, name, success=False)
    return translations.format_cookie_count(ctx, mention=mention, cookie=cookie)


async def gift(ctx: Context, args: tuple):
    translations = ctx.translations.Cookies
    name, amount, *rest = chain(args, repeat(None, 2))
    name = ctx.bot.StringTools.str2name(name) or ctx.author.name

    if name == ctx.bot.nick:
        return translations.gift_bot_nick.format_response(ctx, success=False)
    elif name == ctx.author.name:
        return translations.gift_user_himself.format_response(ctx, success=False)

    cookie_from = await Cookies.get(user=ctx.user)
    user_to = await User.get_or_none(name=name)
    cookie_to = await Cookies.get_or_none(user=user_to)
    if not user_to:
        return translations.user_not_found.format_response(ctx, name, success=False)
    if not cookie_to:
        return translations.cookie_not_found.format_response(ctx, name, success=False)
    cookie_cooldown = await calculate_cooldown(cookie_from)
    on_cooldown = datetime.datetime.now(datetime.UTC) < cookie_from.cooldown
    if on_cooldown and not int(cookie_from.stocked):
        time = ctx.translations.SupportTools.Humanize.precisedelta(cookie_cooldown)
        if not int(cookie_from.stocked):
            return translations.gift_on_cooldown_no_stock.format_response(ctx, time, success=False)

        return translations.daily_limit_reached.format_response(ctx, time, success=False)
    if not amount:
        amount = '1'
    if amount != "all" and not amount.isdigit():
        return translations.invalid_gift_amount.format_response(ctx, amount, success=False)
    if amount == "all":
        await cookie_from.gift_all(cookie_from.stocked, cooldown=on_cooldown)
        await cookie_to.receive_update(cookie_from.stocked)
        return translations.multiple_gift.format_response(ctx, name, cookie_from.stocked)
    amount = int(amount)
    if amount <= cookie_from.stocked:
        await cookie_from.gift(amount, cooldown=on_cooldown)
        await cookie_to.receive_update(amount)
        return translations.gift.format_response(ctx, name, amount)
    elif amount >= cookie_from.stocked:
        amount_available = cookie_from.stocked + cookie_from.not_redeemed()
        time = ctx.translations.SupportTools.Humanize.precisedelta(cookie_from.datetime_to(amount - amount_available))
        return translations.gift_not_enough_cookies.format_response(ctx, success=False)
    # TODO: else: too tired to tink what comes here.


async def stock(ctx: Context, args: tuple):
    translations = ctx.translations.Cookies
    amount, *rest = chain(args, repeat(None, 1))

    if not amount:
        amount = '1'
    if amount != "all" and not amount.isdigit():
        return translations.invalid_gift_amount.format_response(ctx, amount, success=False)

    cookie = await Cookies.get(user=ctx.user)
    cookie_cooldown = await calculate_cooldown(cookie)
    on_cooldown = datetime.datetime.now(datetime.UTC) < cookie.cooldown

    if on_cooldown:
        time = ctx.translations.SupportTools.Humanize.precisedelta(cookie_cooldown)
        return translations.daily_limit_reached.format_response(ctx, time, success=False)
    amount_available = cookie.not_redeemed()
    if amount == "all":
        await cookie.stock_all(amount_available)
        return translations.stock.format_response(ctx, amount_available)
    amount = int(amount)
    if amount <= amount_available:
        await cookie.stock(amount)
        if amount == amount_available:
            return translations.stock.format_response(ctx, amount)
        return translations.stock_not_daily.format_response(ctx, amount)
    elif amount >= amount_available:
        return translations.stock_not_enough_cookies.format_response(ctx, amount_available)
    # TODO: else: too tired to tink what comes here.


async def top(ctx: Context, args: tuple):
    translations = ctx.translations.Cookies
    order_by, *rest = chain(args, repeat(None, 1))
    if order_by not in translations.order_dict:
        return translations.ranks.format_response(ctx, ', '.join(list(translations.order_dict.keys())), success=False)

    order_by, title = translations.order_dict[order_by]

    cookies = await Cookies.all().order_by(f"-{order_by}").prefetch_related("user").limit(10)
    emojis = "🏆🥈🥉🏅🏅"
    top_10ish = [
        f"{emoji} @{cookie.user.name}: ({getattr(cookie, order_by)})"
        for emoji, cookie in zip(emojis, cookies)
    ]
    tops = " ".join(top_10ish)
    cookie_user = await Cookies.get(user=ctx.user)
    user_index = await Cookies.filter(**{f'{order_by}__gt': getattr(cookie_user, order_by)}).count() + 1

    return translations.top10_ish.format_response(ctx,
                                                  len(top_10ish),
                                                  title,
                                                  tops,
                                                  user_index,
                                                  getattr(cookie_user, order_by)
                                                  )


async def slotmachine(ctx: Context, args: tuple):
    ...



def dynamic_description(command_: Command, bot: Gorenmu, ctx: Context = None, ) -> dict[str, dict[str, str]]:
    responses: dict[str, dict[str, str]] = {}
    cooldown_ = command_._cooldowns[0]  # NOQA
    per = cooldown_._per  # NOQA
    rate = cooldown_._rate  # NOQA
    prefix = ctx.prefix if ctx else bot.config.BotConfig.prefix[0]
    for lang in command_.decorators:
        if lang not in responses:
            responses[lang] = {}
        decorator: EnDecorators.Change_Here = command_.decorators[lang]
        description = decorator.get_description(decorator)  # NOQA
        base_decorators = bot.TranslationManager.get_decorator(lang)
        cooldown_type = base_decorators.get_bucket_type(cooldown_.bucket)

        language: EnDecorators = bot.TranslationManager.languages[lang][0]
        command_body_template1: str = getattr(language, 'template_part1', EnDecorators.template_part1)
        command_body_template2: str = getattr(language, 'template_part2', EnDecorators.template_part2)
        command_body_template3: str = getattr(language, 'template_part3', EnDecorators.template_part3)
        alias_template: str = getattr(language, 'alias_template', EnDecorators.alias_template)
        command_template: str = getattr(language, 'command_template', EnDecorators.command_template)
        admonition_template: str = getattr(language, 'admonition_template', EnDecorators.admonition_template)

        aliases = ""
        if command_.aliases:
            aliases = alias_template.format(command_title=command_.name.capitalize(),
                                            aliases=", ".join(command_.aliases)
                                            )

        command_body = command_body_template1.format(
                                            command_title=command_.name.capitalize(),
                                            rate=rate, per=per,
                                            cooldown_type=cooldown_type,
                                            )
        commands_admonitions = getattr(decorator, 'admonitions', EnDecorators.Change_Here.admonitions)

        if commands_admonitions:
            for admonition in commands_admonitions:
                if admonition.position == "top":
                    command_body += admonition_template.format(
                            type=admonition.type,
                            title=admonition.title,
                            message=admonition.message)

        command_body += command_body_template2.format(description=description, aliases=aliases)

        if commands_admonitions:
            for admonition in commands_admonitions:
                if admonition.position == "middle":
                    command_body += admonition_template.format(
                            type=admonition.type,
                            title=admonition.title,
                            message=admonition.message)

        command_body += command_body_template3

        if commands := getattr(decorator, 'commands', EnDecorators.Change_Here.commands):
            command_body += "".join([
                    command_template.format(prefix=prefix, command_name=command_.name.lower(), args=item.args,
                                            response=item.response
                                            ) for item in commands])
        if commands_admonitions:
            for admonition in commands_admonitions:
                if admonition.position == "bottom":
                    command_body += admonition_template.format(
                            type=admonition.type,
                            title=admonition.title,
                            message=admonition.message)

        responses[lang][command_.name.lower()] = command_body

    return responses











