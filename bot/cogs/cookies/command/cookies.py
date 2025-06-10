# -*- coding: utf-8 -*-
from __future__ import annotations

import datetime
import random
from collections import Counter
from itertools import chain, groupby, repeat
from typing import List, TYPE_CHECKING

from bot.ext import commands, Context
from bot.models import Cookies, User
from bot.translations import BaseDecorators, Response
from bot.utils import Check

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class CookieCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.multiplicador = 1

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    async def guards_component(self, ctx: Context) -> bool:
        return await Check.cookie_check(ctx)

    @commands.base_decorator(BaseDecorators.Cookies)
    @commands.group(name="cookies", aliases=["cookie"], invoke_fallback=True)
    async def cookies(self, ctx: Context) -> Response:
        return ctx.user.translations.Cookies.invalid_option.format_response(ctx, success=False)

    @cookies.command(name="eat")
    async def eat(self, ctx: Context, *args):
        translations = ctx.user.translations.Cookies
        amount, *rest = chain(args, repeat(None, 1))
        cookie = await Cookies.get_cookie(ctx)
        amount_available = cookie.not_redeemed()
        amount = self.bot.StringTools.to_amount(amount, 1)
        cookie_cooldown = await calculate_cooldown(cookie)
        if amount == 0:
            return translations.not_eat.format_response(ctx, success=False)
        elif amount < 0:
            return translations.negative_eat.format_response(ctx, amount, success=False)
        elif 1 < amount <= amount_available:
            await cookie.daily_update(amount)
            return translations.multiple_eat.format_response(ctx, amount)
        elif datetime.datetime.now(datetime.UTC) > cookie.cooldown:
            await cookie.daily_update(1)
            choice = ctx.user.translations.Cookies.random_line()  # NOQA
            return translations.eat.format_response(ctx, choice["text"])
        else:
            time = ctx.user.translations.SupportTools.TimeTools.Humanize.precisedelta(cookie_cooldown)
            return translations.daily_limit_reached.format_response(ctx, time, success=False)

    @cookies.command(name="count", aliases=["cc"])
    async def count(self, ctx: Context, *args):
        translations = ctx.user.translations.Cookies
        name, *rest = chain(args, repeat(None, 1))
        name = ctx.bot.StringTools.str2name(name) or ctx.author.name

        support_tools = ctx.user.translations.SupportTools

        mention_str = support_tools.LanguageContext.mention
        mention = mention_str if name == ctx.author.name else f"@{name}"

        if mention == mention_str:
            verb = support_tools.LanguageContext.Verbs.second_person
        else:
            verb = support_tools.LanguageContext.Verbs.third_person

        if name == ctx.bot.bot_nick:
            return translations.cc_bot_nick.format_response(ctx, success=False)
        elif name == ctx.author.name:
            cookie = await Cookies.get_or_none(user=ctx.user)
            return translations.format_cookie_count(ctx, mention=mention, cookie=cookie, verb=verb)  # NOQA

        elif not (user := await User.get_or_none(name=name)):
            return translations.user_not_found.format_response(ctx, name, success=False)
        cookie = await Cookies.get_or_none(user=user)
        return translations.format_cookie_count(ctx, mention=mention, cookie=cookie, verb=verb)  # NOQA

    @cookies.command(name="gift")
    async def gift(self, ctx: Context, *args):
        translations = ctx.user.translations.Cookies
        all_options = [translations.all_string, ctx.bot.TranslationManager.en.strings.Cookies.all_string]
        name, amount, *rest = chain(args, repeat(None, 2))
        name = ctx.bot.StringTools.str2name(name) or ctx.author.name
        if name == ctx.bot.bot_nick:
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
        amount_available = cookie_from.stocked + cookie_from.not_redeemed()
        amount, is_all = ctx.bot.StringTools.to_all(amount, amount_available, all_options, default=1)
        if amount <= 0:
            if amount == 0:
                return translations.not_gifted.format_response(ctx, success=False)
            return translations.negative_gift.format_response(ctx, success=False)
        if on_cooldown and not int(cookie_from.stocked):
            time = ctx.user.translations.SupportTools.TimeTools.Humanize.precisedelta(cookie_cooldown)
            return translations.gift_on_cooldown_no_stock.format_response(ctx, time, success=False)
        if is_all:
            await cookie_from.gift_all(cookie_from.stocked, amount_available)
            await cookie_to.receive_update(amount_available)
            return translations.multiple_gift.format_response(ctx, name, amount_available)
        if amount <= cookie_from.stocked:
            await cookie_from.gift(amount, cooldown=on_cooldown)
            await cookie_to.receive_update(amount)
            if amount == 1:
                return translations.gift.format_response(ctx, name, amount)
            return translations.multiple_gift.format_response(ctx, name, amount)
        elif amount >= cookie_from.stocked and amount_available > 0:
            return translations.gift_no_stock_but_cooldown.format_response(ctx, amount_available, success=False)
        elif amount >= cookie_from.stocked and not amount_available:
            time = ctx.user.translations.SupportTools.TimeTools.Humanize.precisedelta(
                cookie_from.datetime_to(amount - amount_available)
            )
            return translations.gift_on_cooldown_no_stock.format_response(ctx, time, success=False)
        else:
            ctx.bot.log.error("Unexpected status: Unable to process cookie donation.")
            return ctx.user.translations.Exceptions.unexpected_error.format_response(ctx)

    @cookies.command(name="stock")
    async def stock(self, ctx: Context, *args):
        translations = ctx.user.translations.Cookies
        all_options = [translations.all_string, ctx.bot.TranslationManager.en.strings.Cookies.all_string]
        amount, *rest = chain(args, repeat(None, 1))

        cookie = await Cookies.get(user=ctx.user)
        cookie_cooldown = await calculate_cooldown(cookie)
        on_cooldown = datetime.datetime.now(datetime.UTC) < cookie.cooldown
        amount_available = cookie.not_redeemed()
        amount, is_all = ctx.bot.StringTools.to_all(amount, amount_available, all_options, default=1)

        if on_cooldown:
            time = ctx.user.translations.SupportTools.TimeTools.Humanize.precisedelta(cookie_cooldown)
            return translations.daily_limit_reached.format_response(ctx, time, success=False)

        if is_all:
            await cookie.stock_all(amount_available)
            return translations.stock.format_response(ctx, amount_available)
        if amount <= amount_available:
            await cookie.stock(amount)
            if amount == amount_available:
                return translations.stock.format_response(ctx, amount)
            return translations.stock_not_daily.format_response(ctx, amount)
        elif amount >= amount_available:
            return translations.stock_not_enough_cookies.format_response(ctx, amount_available)
        else:
            ctx.bot.log.error("Unexpected status: Unable to process cookie donation.")
            return ctx.user.translations.Exceptions.unexpected_error.format_response(ctx)

    @cookies.command(name="top")
    async def top(self, ctx: Context, *args):
        translations = ctx.user.translations.Cookies
        order_by, *rest = chain(args, repeat(None, 1))
        if order_by not in translations.order_dict:
            return translations.ranks.format_response(
                ctx, ", ".join(list(translations.order_dict.keys())), success=False
            )

        order_by, title = translations.order_dict[order_by]

        cookies = await Cookies.all().order_by(f"-{order_by}").prefetch_related("user").limit(10)
        emojis = "🏆🥈🥉🏅🏅"
        top_10ish = [
            f"{emoji} @{cookie.user.name}: ({getattr(cookie, order_by)})" for emoji, cookie in zip(emojis, cookies)
        ]
        tops = " ".join(top_10ish)
        cookie_user = await Cookies.get(user=ctx.user)
        user_index = await Cookies.filter(**{f"{order_by}__gt": getattr(cookie_user, order_by)}).count() + 1

        return translations.top10_ish.format_response(
            ctx, len(top_10ish), title, tops, user_index, getattr(cookie_user, order_by)
        )

    @cookies.command(name="sm", aliases=["slotmachine"])
    async def slotmachine(self, ctx: Context, amount: str = "1"):
        user = ctx.user
        translations = user.translations.Cookies
        all_options = [translations.all_string, ctx.bot.TranslationManager.en.strings.Cookies.all_string]

        await user.fetch_related("cookies")
        cookie = await Cookies.get_cookie(ctx)

        if await _is_on_cooldown(cookie):
            return await _cooldown_response(ctx, cookie)

        amount_available = cookie.not_redeemed()
        parsed_amount, is_all = ctx.bot.StringTools.to_all(amount, amount_available, all_options, default=1)

        if parsed_amount is None:
            return translations.invalid_amount.format_response(ctx, amount, amount_available)

        fruits = _get_fruit_emojis()
        emotes = await _get_emotes(ctx, fruits)

        rewards = await get_rewards(ctx, emotes)
        time_suffix = await parse_time(amount_available, ctx, is_all, translations)
        amount_label = f"{translations.all_string} {parsed_amount}" if is_all else parsed_amount

        total_reward, reward_counts, sequences = await all_slotmachine(
            fruits=emotes, rewards=rewards, quantidade=parsed_amount
        )

        reward_counts = sorted(reward_counts.items())  # NOQA
        # TODO Future: show reward breakdown.
        # breakdown = ", ".join([f"{count} of {value}" for value, count in reward counts])

        is_all_mode = not parsed_amount.is_integer() and is_all
        stock_method = cookie.stock_all if is_all_mode else cookie.stock

        if total_reward:
            emote = (await self.bot.Emotes.get_pog(channel_id=ctx.channel.id, user=user))[0]
            total = total_reward * self.multiplicador
            await stock_method(amount_available)  # NOQA
            suffix = translations.cookie_win_suffix.format(total, time_suffix)
        else:
            emote = (await self.bot.Emotes.get_sad(channel_id=ctx.channel.id, user=user))[0]
            await stock_method(0)  # NOQA
            suffix = translations.cookie_loss_suffix.format(time_suffix)

        if parsed_amount == 1 and total_reward and len(sequences) == 1:
            prefix = f'[ {" | ".join(sequences[0])} ]'
        else:
            prefix = ""

        if is_all_mode or amount_available != 1:
            return translations.accumulated_message.format_response(ctx, prefix, amount_label, suffix, emote)
        else:
            return translations.last_cookie_message.format_response(ctx, prefix, suffix, emote)


async def parse_time(amount_available, ctx, is_all, translations):
    if is_all or amount_available == 1:
        time = ctx.user.translations.SupportTools.TimeTools.Humanize.precisedelta(datetime.timedelta(hours=6))
        time_suffix = translations.time_suffix.format(time)
    else:
        time_suffix = ""
    return time_suffix


async def get_rewards(ctx: Context, frutas: list):
    rewards = await ctx.bot.cache.get(key=int(ctx.broadcaster.id), namespace="cookies_rewards")
    if not rewards:
        levels = [5, 4, 3, 2]
        points = {5: 30, 4: 12, 3: 6, 2: 3}
        rewards = {(level, fruta): points[level] for level in levels for fruta in frutas}
        await ctx.bot.cache.set(
            key=int(ctx.broadcaster.id),
            value=rewards,
            namespace="cookies_rewards",
            ttl=datetime.timedelta(hours=6).total_seconds(),
        )
    return rewards


async def calculate_cooldown(cookie: Cookies):
    if not cookie.cooldown:
        cookie.cooldown = datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=8, seconds=10)
        await cookie.save()
    return datetime.datetime.now(datetime.UTC) - cookie.cooldown


async def calculate_reward(sequencia, recompensas, comprimento_sequencia):
    total_recompensa = 0
    for elemento, grupo in groupby(sequencia):
        tamanho = sum(1 for _ in grupo)
        if tamanho >= comprimento_sequencia:
            total_recompensa += recompensas.get((tamanho, elemento), 0)
    return total_recompensa


async def all_slotmachine(fruits: List[str], rewards: dict[tuple[int, str], int], quantidade):
    sequencias = [random.choices(fruits, k=5) for _ in range(quantidade)]
    recompensas_valores = [await calculate_reward(sequencia, rewards, 2) for sequencia in sequencias]
    soma_total = sum(recompensas_valores)
    contagem_valores = Counter(recompensas_valores)
    return soma_total, contagem_valores, sequencias


async def _is_on_cooldown(cookie) -> bool:
    now = datetime.datetime.now(datetime.UTC)
    return now < cookie.cooldown


async def _cooldown_response(ctx: Context, cookie) -> Response:
    cooldown_duration = await calculate_cooldown(cookie)
    time_str = ctx.user.translations.SupportTools.TimeTools.Humanize.precisedelta(cooldown_duration)
    return ctx.user.translations.Cookies.daily_limit_reached.format_response(ctx, time_str, success=False)


def _get_fruit_emojis() -> list[str]:
    return ["🍇", "🍊", "🍋", "🍒", "🍉", "🍓", "🍌", "🍍", "🥕", "🍆", "🌽", "🥔", "🌶️", "🫑", "🥑"]


async def _get_emotes(ctx: Context, fallback_fruits: list[str]) -> list[str]:
    emotes = await ctx.bot.Emotes.get_random_by_amount(channel_id=ctx.channel.id, amount=len(fallback_fruits))

    if len(emotes) < len(fallback_fruits):
        missing = len(fallback_fruits) - len(emotes)
        fallback = random.sample(fallback_fruits, k=missing)
        emotes += fallback

    return emotes


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(CookieCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
