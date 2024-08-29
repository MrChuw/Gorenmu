# -*- coding: utf-8 -*-
import random
import re

from bot.bot import Gorenmu
from bot.ext.commands import base_decorator, Bucket, check, command, Command, Context, cooldown
from bot.translations import EnDecorators, Response


@base_decorator(EnDecorators.Choice)
@cooldown(rate=3, per=10, bucket=Bucket.user)
@check([])
@command(name='choice', aliases=['pick'])
async def command(ctx: Context, *, content: str) -> Response:
    pattern = '|'.join(map(re.escape, ctx.translations.Choice.choice_separators))
    choice = random.choice([arg for arg in re.split(pattern, content) if arg])
    return ctx.translations.Choice.chosen_option.format_response(ctx, choice)


def dynamic_description(command_: Command, bot: Gorenmu, ctx: Context = None, ) -> dict[str, dict[str, str]]:
    responses: dict[str, dict[str, str]] = {}
    cooldown_ = command_._cooldowns[0]  # NOQA
    per = cooldown_._per  # NOQA
    rate = cooldown_._rate  # NOQA
    prefix = ctx.prefix if ctx else bot.config.BotConfig.prefix[0]
    for lang in command_.decorators:
        if lang not in responses:
            responses[lang] = {}
        decorator: EnDecorators.Choice = command_.decorators[lang]
        description = decorator.get_description(decorator)  # NOQA
        base_decorators = bot.TranslationManager.get_decorator(lang)
        cooldown_type = base_decorators.get_bucket_type(cooldown_.bucket)
        afk_template = getattr(decorator, 'template', EnDecorators.Choice.template).format(rate=rate, per=per,
                cooldown_type=cooldown_type, description=description, command_title=command_.name.capitalize(),
                command_name=command_.name.lower(), prefix=prefix, aliases=", ".join(command_.aliases)
        )

        responses[lang][command_.name.lower()] = afk_template

    return responses
