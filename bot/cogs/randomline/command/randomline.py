# -*- coding: utf-8 -*-
import random

from bot.bot import Gorenmu
from bot.ext.commands import base_decorator, Bucket, check, command, Command, Context, cooldown
from bot.models import Channel, MessagesLog, User
from bot.translations import EnDecorators, Response


async def get_user(ctx: Context, user: str) -> User | None:
    if user.lower() is ctx.author.name.lower():
        user = ctx.user
    else:
        user = await User.get_or_none(name=user)
    return user


async def get_channel(ctx: Context, channel: str) -> Channel | None:
    if channel.lower() in ctx.bot.channels:
        channel = ctx.bot.channels[channel]
        return channel
    return None


async def get_random_message(user=None, channel=None):
    query = MessagesLog.filter()
    if user:
        query = query.filter(user=user)
    if channel:
        query = query.filter(channel=channel)

    count = await query.count()
    if not count or count == 0:
        return None, 0

    value = random.randint(0, count - 1)
    message = await query.offset(value).limit(1).first().prefetch_related("user")
    return message, count


@base_decorator(EnDecorators.RandomLine)
@cooldown(rate=3, per=10, bucket=Bucket.user)
@check([])
@command(name='randomline', aliases=['rl'])
async def command(ctx: Context, *, options: str = "") -> Response:
    translations = ctx.translations.RandomLine
    options_splited = options.split(" ")

    channel_original = next((opt.replace("channel:", "") for opt in options_splited if "channel:" in opt), None)
    user_original = next((opt.replace("user:", "") for opt in options_splited if "user:" in opt), None)

    user, channel = None, None
    if user_original:
        user = await get_user(ctx, user_original)
        if not user:
            return translations.user_not_found.format_response(ctx, user_original)

    if channel_original:
        channel = await get_channel(ctx, channel_original)
        if not channel:
            return translations.channel_not_found.format_response(ctx, channel_original)

    channel = await get_channel(ctx, ctx.channel.name)

    message, count = await get_random_message(user=user, channel=channel)
    if not count:
        return translations.no_message_found.format_response(ctx, user_original or "",
                                                             channel_original or ctx.channel.name
                                                             )

    return translations.random_line.format_response(ctx, message.content, message.created_a_time(ctx),
                                                    message.user.nickname or message.user.name
                                                    )


def dynamic_description(command_: Command, bot: Gorenmu, ctx: Context = None, ) -> dict[str, dict[str, str]]:
    responses: dict[str, dict[str, str]] = {}
    cooldown_ = command_._cooldowns[0]  # NOQA
    per = cooldown_._per  # NOQA
    rate = cooldown_._rate  # NOQA
    prefix = ctx.prefix if ctx else bot.config.BotConfig.prefix[0]
    for lang in command_.decorators:
        if lang not in responses:
            responses[lang] = {}
        decorator: EnDecorators.RandomLine = command_.decorators[lang]
        description = decorator.get_description(decorator)  # NOQA
        base_decorators = bot.TranslationManager.get_decorator(lang)
        cooldown_type = base_decorators.get_bucket_type(cooldown_.bucket)
        afk_template = getattr(decorator, 'template', EnDecorators.RandomLine.template).format(
                rate=rate, per=per,
                cooldown_type=cooldown_type, description=description, command_title=command_.name.capitalize(),
                command_name=command_.name.lower(), prefix=prefix, aliases=", ".join(command_.aliases)
        )

        responses[lang][command_.name.lower()] = afk_template

    return responses
