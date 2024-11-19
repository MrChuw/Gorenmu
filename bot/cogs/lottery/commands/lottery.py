# -*- coding: utf-8 -*-
from typing import List

from bot.bot import Gorenmu
from bot.ext.commands import base_decorator, Bucket, check, command, Command, Context, cooldown
from bot.models import Cookies, Lottery, LotteryBank
from bot.translations import BaseDecorators, Response
from bot.utils import Check
from itertools import combinations
import random


@base_decorator(BaseDecorators.Lottery)
@cooldown(rate=100, per=10, bucket=Bucket.user)
@check([Check.cookie_check, Check.lottery_seed])
@command(name='lottery', aliases=[])
async def command(ctx: Context, option: str = "", *, content: str = "") -> Response:
    if option in ["create"]:
        return await create(ctx, content)
    elif option in ["check"]:
        return await check(ctx, content)
    else:
        return ctx.translations.Lottery.unknown_option.format_response(ctx)


async def check_numbers_async(ctx: Context, content: str) -> Response | List[int]:
    translations = ctx.translations.Lottery
    numbers = content.replace(",", "").split(" ")
    if not all(map(lambda x: x.isdigit() and 1 <= int(x) <= 60, numbers)):
        return translations.only_numbers.format_response(ctx, success=False)
    if len(set(numbers)) != len(numbers):
        return translations.duplicate_numbers.format_response(ctx, success=False)
    if len(numbers) < 3:
        return translations.minimum_bet.format_response(ctx, success=False)
    return list(map(int, numbers))


async def save_lottery_bank(lottery: LotteryBank, value: int):
    lottery.quantity += value
    await lottery.save()


async def create(ctx: Context, content: str) -> Response:
    translations = ctx.translations.Lottery
    if ctx.bot.lottery_lock.locked():
        return translations.lottery_lock.format_response(ctx)
    if (cookies := await Cookies.get(id=int(ctx.author.id))).stocked < 5:
        return translations.not_enough_cookies.format_response(ctx, success=False)
    if content == "random":
        numbers = list(range(1, 61))
        random.shuffle(numbers)
        content = " ".join(str(number) for number in random.sample(numbers, 6))
    if type(numbers := await check_numbers_async(ctx, content)) is not list:
        return numbers



    bet_data = translations.bets_values[len(numbers)]
    value_need = bet_data * len(list(combinations(numbers, 6))) if len(numbers) >= 7 else 5
    last_lottery = await LotteryBank.get(closed=False)
    if cookies.stocked < value_need and len(numbers) <= 6:
        return translations.not_enough_cookies.format_response(ctx, success=False)
    elif cookies.stocked > value_need and len(numbers) <= 6:
        bet = await Lottery.create(user=ctx.user, bet_value=value_need, numbers=numbers, closed=False, earned=0,
                                   draw=last_lottery
                                   )
        await cookies.lottery_update(value=value_need)
        await save_lottery_bank(last_lottery, value_need)
        return translations.bet_place.format_response(ctx, numbers, value_need, bet.id)
    elif cookies.stocked < value_need and 7 <= len(numbers) <= 15:
        return translations.not_enough_cookies_more_five.format_response(ctx, value_need, success=False)
    elif cookies.stocked > value_need and 7 <= len(numbers) <= 15:
        bet = await Lottery.create(user=ctx.user, bet_value=value_need, numbers=numbers, closed=False, earned=0,
                                   draw=last_lottery
                                   )
        await cookies.lottery_update(value=value_need)
        await save_lottery_bank(last_lottery, value_need)
        return translations.bet_place.format_response(ctx, numbers, value_need, bet.id)
    else:
        return translations.too_much_numbers.format_response(ctx, success=False)


async def check(ctx: Context, content: str) -> Response:
    translations = ctx.translations.Lottery
    ids = []
    bets_total = 0
    if content.isdigit():
        bet = await Lottery.get_or_none(id=int(content), user=ctx.user)
        if not bet:
            return translations.no_bet_id.format_response(ctx, success=False)
        time = bet.created_a_time(ctx.translations.SupportTools.Humanize, ctx.user.timezone_)
        return translations.ticket_info.format_response(ctx, bet.numbers, bet.bet_value, time)
    elif "old" in translations.past:
        bets: list[Lottery] = await Lottery.filter(user=ctx.user, closed=True)
        if not bets:
            return translations.no_old_bets_found.format_response(ctx)
        for bet in bets:
            ids.append(bet.id)
            bets_total += bet.bet_value
        return translations.old_bets.format_response(ctx, ids, bets_total)
    elif "new" in translations.current:
        bets: list[Lottery] = await Lottery.filter(user=ctx.user, closed=False)
        if not bets:
            return translations.no_active_bets_found.format_response(ctx)
        for bet in bets:
            ids.append(bet.id)
            bets_total += bet.bet_value
        return translations.active_bets.format_response(ctx, ids, bets_total)
    else:
        bets: list[Lottery] = await Lottery.filter(user=ctx.user)
        if not bets:
            return translations.no_bets.format_response(ctx)
        for bet in bets:
            ids.append(bet.id)
            bets_total += bet.bet_value
        return translations.all_bets.format_response(ctx, ids, bets_total)


def dynamic_description(command_: Command, bot: Gorenmu, ctx: Context = None) -> dict[str, dict[str, str]]:
    responses: dict[str, dict[str, str]] = {}
    cooldown_ = command_._cooldowns[0]  # NOQA
    per = cooldown_._per  # NOQA
    rate = cooldown_._rate  # NOQA
    prefix = ctx.prefix if ctx else bot.config.BotConfig.prefix[0]
    for lang in command_.decorators:
        if lang not in responses:
            responses[lang] = {}
        decorator: EnDecorators.Lottery = command_.decorators[lang]
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

        command_body = command_body_template1.format(command_title=command_.name.capitalize(), rate=rate, per=per,
                                                     cooldown_type=cooldown_type)
        commands_admonitions = getattr(decorator, 'admonitions', EnDecorators.Lottery.admonitions)

        if commands_admonitions:
            for admonition in commands_admonitions:
                if admonition.position == "top":
                    command_body += admonition_template.format(type=admonition.type, title=admonition.title,
                                                               message=admonition.message)

        command_body += command_body_template2.format(description=description, aliases=aliases)

        if commands_admonitions:
            for admonition in commands_admonitions:
                if admonition.position == "middle":
                    command_body += admonition_template.format(type=admonition.type, title=admonition.title,
                                                               message=admonition.message)

        command_body += command_body_template3

        if commands := getattr(decorator, 'commands', EnDecorators.Lottery.commands):
            command_body += "".join([
                    command_template.format(prefix=prefix, command_name=command_.name.lower(), args=item.args,
                                            response=item.response
                                            ) for item in commands])
        if commands_admonitions:
            for admonition in commands_admonitions:
                if admonition.position == "bottom":
                    command_body += admonition_template.format(type=admonition.type, title=admonition.title,
                                                               message=admonition.message)

        responses[lang][command_.name.lower()] = command_body

    return responses
