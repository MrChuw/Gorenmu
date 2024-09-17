# -*- coding: utf-8 -*-
import asyncio
import datetime
import random
from itertools import combinations

from bot.bot import Gorenmu
from bot.ext import routine
from bot.models import Channel, Lottery, LotteryBank, Reminder, User

time_util_lottery = 1800
# time_util_lottery = 150
points_for_hits = {3: 1, 4: 2, 5: 3, 6: 5}


# TODO: change to saturday
@routine(wait_first=True, weekly_days=[5],
         weekly_times=[datetime.time(hour=12)]
         )
# @routine(seconds=30)
async def routine(bot: Gorenmu) -> None:
    bot.log.info("Lottery routine has started.")
    bot_user = await User.get_or_none(id=bot.user_id)
    bank: LotteryBank = await LotteryBank.filter(closed=False).first()
    current_prize_pool = bank.quantity + bank.accumulated_quantity
    await execute_announcements(bot, current_prize_pool)
    async with bot.lottery_lock:
        valid_bets = []
        invalid_bets = []
        winners = {}
        numbers = list(range(1, 61))
        random.shuffle(numbers)
        drawn_numbers = set(random.sample(numbers, 6))

        all_tickets: list[Lottery] = await Lottery.filter(draw=bank).all().prefetch_related("user").prefetch_related(
                "user__cookies"
        )

        for ticket in all_tickets:
            if not ticket.draw_sorted_numbers:
                ticket.draw_sorted_numbers = []
            cards = calculate_cards(ticket.numbers)
            for card in cards:
                hits = calculate_hits(card, drawn_numbers)
                ticket.draw_sorted_numbers.append(list(set(card) & drawn_numbers))
                if hits >= 3:
                    valid_bets.append((ticket, hits))
                else:
                    invalid_bets.append((ticket, hits))

        total_points = sum(points_for_hits[acertos] for _, acertos in valid_bets)

        for ticket, hits in valid_bets:
            proportion = points_for_hits[hits] / total_points
            gain = proportion * current_prize_pool
            if ticket.user.name not in winners:
                winners[ticket.user.name] = Winner(
                        **{"user": ticket.user, "tickets": [ticket], "hits": hits, "gain": int(gain)}
                )
            else:
                winners[ticket.user.name].gain += int(gain)
                winners[ticket.user.name].tickets.append(ticket)
            ticket.earned += int(gain)
            ticket.closed = True
            ticket.closed_in = datetime.datetime.now()

        for ticket, hits in invalid_bets:
            ticket.earned = 0
            ticket.closed = True
            ticket.closed_in = datetime.datetime.now()

        for winner in winners:
            winner = winners[winner]
            translation = bot.TranslationManager.get_translations(winner.user.language).Lottery
            ids = ", ".join(str(ticket.id) for ticket in winner.tickets)
            message = translation.remind_message.format(winner.gain, [ids])
            await Reminder.create(from_user=bot_user, to_user=winner.user, content=message)
            await winner.user.cookies[0].lottery_update(winner.gain)

        bank.closed = True
        bank.closed_in = datetime.datetime.now()
        bank.accumulated = not winners

        await LotteryBank.create(accumulated_quantity=0 if winners else current_prize_pool, accumulated=not winners
                                 )
        await bank.save()
        for ticket in all_tickets:
            await ticket.save()

        await announce_results(bot, list(drawn_numbers), False if winners else current_prize_pool)


class Winner:
    def __init__(self, user: User, tickets: list[Lottery], hits: list[list[int]], gain: int):
        self.user: User = user
        self.tickets: list[Lottery] = tickets
        self.hits: list[list[int]] = hits
        self.gain: int = gain


async def announce_results(bot: Gorenmu, numbers: list[int], total: int = None):
    for channel_name in bot.channels:
        channel: Channel = bot.channels[channel_name]
        translation = bot.TranslationManager.get_translations(channel.language).Lottery
        if channel.online and "lottery notice" not in channel.disabled:
            await asyncio.sleep(0.2)
            lottery_result_announce = translation.lottery_result_announce
            if not total:
                message = lottery_result_announce.format(translation.winners.format(numbers))
            else:
                message = lottery_result_announce.format(translation.no_winners.format(numbers, total))
            await bot.get_channel(channel_name).send(message)


async def announce(bot: Gorenmu, current_prize_pool: int, message_number: int):
    for channel_name in bot.channels:
        channel: Channel = bot.channels[channel_name]
        translation = bot.TranslationManager.get_translations(channel.language).Lottery
        if channel.online and "lottery notice" not in channel.disabled:
            await asyncio.sleep(0.2)
            if message_number == 0:
                await bot.get_channel(channel_name).send(
                        translation.lottery_announce_messages[message_number].format(current_prize_pool, channel.prefix)
                )
            else:
                await bot.get_channel(channel_name).send(translation.lottery_announce_messages[message_number])


async def execute_announcements(bot: Gorenmu, current_prize_pool):
    while True:
        await announce(bot, current_prize_pool, 0)
        await asyncio.sleep(time_util_lottery / 2)
        await announce(bot, current_prize_pool, 1)
        await asyncio.sleep((time_util_lottery / 2) - 60)
        await announce(bot, current_prize_pool, 2)
        await asyncio.sleep(50)
        await announce(bot, current_prize_pool, 3)
        break


def calculate_hits(player_numbers, drawn_numbers):
    return len(set(player_numbers) & drawn_numbers)


def calculate_cards(player_numbers):
    if len(player_numbers) <= 6:
        return [player_numbers]
    else:
        return list(combinations(player_numbers, 6))
