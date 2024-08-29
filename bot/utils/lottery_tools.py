# -*- coding: utf-8 -*-
from __future__ import annotations

import asyncio
from typing import List, Tuple, TYPE_CHECKING

from twitchio import Message

from bot.ext.commands import Context
from bot.models import (Cookies as CookieModel, Lottery, LotteryBank)
from bot.translations import EnDecorators
from bot.translations import Response

if TYPE_CHECKING:
    from bot.bot import Gorenmu

betting_values: dict = {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 11, 8: 25, 9: 63, 10: 187, 11: 346, 12: 649, 13: 943,
                        14: 1038, 15: 1294,
                        }


class LotteryTools:  # TODO: Lottery.
    def __init__(self, bot: Gorenmu):
        self.bot = bot
        self.valor_aposta = 5
        self.multiplier = 1.87
        self.lock: asyncio.Lock = asyncio.Lock()

    @staticmethod
    def check_bet_or_consultation(message: Message, ctx: Context):
        if message.echo:
            return False
        if message.channel.name != ctx.channel.name:
            return False
        if message.author.id != ctx.author.id:
            return False
        if message.content.lower() in ctx.translations.SupportTools.Lottery.bet_or_consultation:
            return True
        if message.content.lower().startswith("ticket"):
            return True
        return False

    @staticmethod
    def check_numbers(message: Message, ctx: Context, translations: EnDecorators.Lottery.Lottery) -> (
            bool | Tuple[bool, List[int]]):
        if message.echo:
            return False
        if message.channel.name != ctx.channel.name:
            return False
        if message.author.id != ctx.author.id:
            return False
        numbers = message.content.replace(",", "").split(" ")
        # Não sei se isso de simple response funciona.
        if not all(map(lambda x: x.isdigit() and 1 <= int(x) <= 60, numbers)):
            ctx.bot.loop.create_task(ctx.simple_response(ctx, translations.only_numbers.response))
            return False
        if len(set(numbers)) != len(numbers):
            ctx.bot.loop.create_task(ctx.simple_response(ctx, translations.duplicate_numbers.response))
            return False
        if len(numbers) < 3:
            ctx.bot.loop.create_task(ctx.simple_response(ctx, translations.minimum_bet.response))
            return False
        return True, numbers

    @staticmethod
    async def check_numbers_async(ctx: Context, translations: EnDecorators.Lottery.Bet) -> Response | List[int]:
        numbers = ctx.message.content.replace(",", "").split(" ")
        numbers.pop(0)
        if not all(map(lambda x: x.isdigit() and 1 <= int(x) <= 60, numbers)):
            return translations.only_numbers.format_response(ctx, success=False)
        if len(set(numbers)) != len(numbers):
            return translations.duplicate_numbers.format_response(ctx, success=False)
        if len(numbers) < 3:
            return translations.minimum_bet.format_response(ctx, success=False)
        return numbers

    async def bet(self, ctx: Context, translations: EnDecorators.Lottery.Lottery) -> Response:
        if (cookies := await CookieModel.get(id=int(ctx.author.id))).stocked < 5:
            return translations.not_enough_cookies.format_response(ctx, success=False)
        await ctx.simple_response(ctx, translations.bet_message)

        def check_numbers_proxy(message: Message):
            return self.check_numbers(message, ctx, translations)

        try:
            response = await self.bot.wait_for("message", check_numbers_proxy, timeout=30)
        except asyncio.TimeoutError:
            return translations.timeout.format_response(ctx, success=False)
        else:
            response: Message = response[0]
            numbers = list(map(int, response.content.split(" ")))
            last_bet = await LotteryBank.get(closed=False)
            if len(numbers) <= 6:
                if cookies.stocked < self.valor_aposta:
                    return translations.not_enough_cookies.format_response(ctx, success=False)
                else:
                    await Lottery.create(user=ctx.user, bet_value=5, numbers=numbers, closed=False, earned=0,
                                         draw_id=last_bet.id, )
                    await cookies.reduce_update(value=5)
                    await last_bet.add(value=5)
                    return translations.five_numbers_bet.format_response(ctx, response, success=True)
            elif 7 <= len(numbers) <= 15:
                if cookies.stocked < self.valor_aposta * self.multiplier:
                    return translations.not_enough_cookies.format_response(ctx, success=False)
                else:
                    bet_value: int = betting_values[len(numbers)]
                    await Lottery.create(user=ctx.user, bet_value=bet_value, numbers=numbers, closed=False, earned=0,
                                         draw_id=last_bet.id, )
                    await cookies.reduce_update(value=bet_value)
                    await last_bet.add(value=bet_value)
                    return translations.more_than_five_numbers_bet.format_response(ctx, response, bet_value,
                                                                                   success=True
                                                                                   )
            else:
                return translations.too_much_numbers.format_response(ctx, success=False)

    async def consultation(self, ctx: Context, translations: EnDecorators.Lottery.Lottery) -> Response:
        ids = []
        value = 0
        await ctx.simple_response(ctx, translations.consultation_message)

        # Removido
        def checkPassadasAtuaisProxy(message: Message):
            # return self.check_passadas_ou_atuais(message, ctx)
            ...

        try:
            response = await self.bot.wait_for("message", checkPassadasAtuaisProxy, timeout=30)
        except asyncio.TimeoutError:
            return translations.timeout.format_response(ctx, success=False)
        else:
            response: Message = response[0]
            if response.content.lower() == translations.past:
                bets = await Lottery.filter(user=ctx.user, encerrada=True)
                for bet in bets:
                    bet: Lottery
                    ids.append(bet.id)
                    value += bet.bet_value
                return translations.old_bets.format_response(ctx, len(bets), value, ids, success=True)
            elif response.content.lower() == translations.current:
                bets = await Lottery.filter(user=ctx.user, encerrada=False)
                for bet in bets:
                    bet: Lottery
                    ids.append(bet.id)
                    value += bet.bet_value
                if len(bets) == 0:
                    return translations.no_bets_next_lottery.format_response(ctx, success=True)
                return translations.new_bets.format_response(ctx, len(bets), value, ids, success=True)
            else:
                return translations.invalid_option.format_response(ctx, success=False)
