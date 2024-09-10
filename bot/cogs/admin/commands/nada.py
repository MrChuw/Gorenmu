# -*- coding: utf-8 -*-
import asyncio
import datetime
from bot.bot import Gorenmu
from bot.models import User, Channel
from bot.utils import Check, Role
from typing import Dict, Any, List, Tuple, Optional, Coroutine, Callable
from bot.ext.commands import Bucket, check, Context, cooldown, base_decorator, helper, usage, command, Command
from bot.translations import EnTranslations, EnDecorators, Response



@base_decorator(EnDecorators.Admin.Nada)
@cooldown(rate=3, per=10, bucket=Bucket.user)
@check([Role.dev])
@command(name='nada', aliases=[])
async def command(ctx: Context, *, args, ) -> Response:
    translations = ctx.translations.Admin.Nada()
    teste = datetime.datetime.now(datetime.timezone.utc)

    return translations.nada.format_response(ctx, args, success=True, handle=None, response_list=[])



def dynamic_description(command_: Command, bot: Gorenmu, ctx: Context = None, ) -> dict[str, dict[str, str]]:
    responses: dict[str, dict[str, str]] = {}
    cooldown_ = command_._cooldowns[0]  # NOQA
    per = cooldown_._per  # NOQA
    rate = cooldown_._rate  # NOQA
    prefix = ctx.prefix if ctx else bot.config.BotConfig.prefix[0]
    for lang in command_.decorators:
        if lang not in responses:
            responses[lang] = {}
        decorator: EnDecorators.Admin.Nada = command_.decorators[lang]
        description = decorator.get_description(decorator)  # NOQA
        base_decorators = bot.TranslationManager.get_decorator(lang)
        cooldown_type = base_decorators.get_bucket_type(cooldown_.bucket)
        language: EnDecorators = bot.TranslationManager.languages[lang][0]
        command_body_template = getattr(language, 'template', EnDecorators.template)
        alias_template = getattr(language, 'alias_template', EnDecorators.alias_template)
        command_template = getattr(language, 'command_template', EnDecorators.command_template)
        admonition_template = getattr(language, 'admonition_template', EnDecorators.admonition_template)

        aliases = ""
        if command_.aliases:
            aliases = alias_template.format(command_title=command_.name.capitalize(),
                                            aliases=", ".join(command_.aliases))

        command_body = command_body_template.format(
                command_title=command_.name.capitalize(),
                rate=rate,
                per=per,
                description=description,
                cooldown_type=cooldown_type,
                aliases=aliases)

        command_responses = ""
        if commands := getattr(decorator, 'commands', EnDecorators.Admin.Nada.commands):
            command_responses = "".join([command_template.format(
                    prefix=prefix,
                    command_name=command_.name.lower(),
                    args=item.args,
                    response=item.response
            ) for item in commands])

        admonitions = ""
        if commands_admonitions := getattr(decorator, 'admonitions', EnDecorators.Admin.Nada.admonitions):
            admonitions = "".join([admonition_template.format(
                    type=admonition.type,
                    title=admonition.title,
                    message=admonition.message,
            ) for admonition in commands_admonitions])

        responses[lang][command_.name.lower()] = command_body + command_responses + admonitions

    return responses



