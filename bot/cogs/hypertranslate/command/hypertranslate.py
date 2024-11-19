# -*- coding: utf-8 -*-
import asyncio
import random

from bot.apis import GoogleTranslator
from bot.apis.translate.constants import GOOGLE_LANGUAGES_TO_CODES as GOOGLE_LANGS
from bot.apis.translate.exceptions import TooManyRequests
from bot.bot import Gorenmu
from bot.ext.commands import base_decorator, Bucket, check, command, Command, Context, cooldown
from bot.translations import BaseDecorators, BaseTranslations, Response


@base_decorator(BaseDecorators.HyperTranslate)
@cooldown(rate=3, per=10, bucket=Bucket.user)
@check([])
@command(name='hypertranslate', aliases=['ht'])
async def command(ctx: Context, quantity: str = None, *, content: str = "") -> Response:
    translations = ctx.translations.HyperTranslate()
    session = ctx.bot.SessionsCaches.TranslateCachedSession.session
    if not quantity.isdigit():
        return translations.quantity_error.format_response(ctx, ctx.prefix, success=False)
    sleep = 0 if int(quantity) > 500 else 0.5
    runs = 0
    quantity = int(quantity)
    await ctx.simple_response(ctx, translations.starter_string)
    while True:
        try:
            if runs == quantity + 1:
                break
            await asyncio.sleep(sleep)
            target = (
                    BaseTranslations.HyperTranslate.lang if runs == quantity - 1 else translations.lang if runs == quantity else random.choice(
                        list(GOOGLE_LANGS.values())
                        ))
            translator = GoogleTranslator(session=session, target=target)
            content = await translator.translate(content)
            runs += 1
        except TooManyRequests as e:
            ctx.bot.log.warning(e)
            await asyncio.sleep(60)
        except Exception as e:
            ctx.bot.log.error(e)
            await asyncio.sleep(10)
    if not content:
        return translations.unexpected_error.format_response(ctx, success=False)
    return translations.translation.format_response(ctx, content)


def dynamic_description(command_: Command, bot: Gorenmu, ctx: Context = None, ) -> dict[str, dict[str, str]]:
    responses: dict[str, dict[str, str]] = {}
    cooldown_ = command_._cooldowns[0]  # NOQA
    per = cooldown_._per  # NOQA
    rate = cooldown_._rate  # NOQA
    prefix = ctx.prefix if ctx else bot.config.BotConfig.prefix[0]
    for lang in command_.decorators:
        if lang not in responses:
            responses[lang] = {}
        decorator: EnDecorators.HyperTranslate = command_.decorators[lang]
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
                                                     cooldown_type=cooldown_type, )
        commands_admonitions = getattr(decorator, 'admonitions', EnDecorators.HyperTranslate.admonitions)
        if commands_admonitions:
            for admonition in commands_admonitions:
                if admonition.position == "top":
                    command_body += admonition_template.format(type=admonition.type, title=admonition.title,
                                                               message=admonition.message
                                                               )

        command_body += command_body_template2.format(description=description, aliases=aliases)

        if commands_admonitions:
            for admonition in commands_admonitions:
                if admonition.position == "middle":
                    command_body += admonition_template.format(type=admonition.type, title=admonition.title,
                                                               message=admonition.message
                                                               )

        command_body += command_body_template3

        if commands := getattr(decorator, 'commands', EnDecorators.HyperTranslate.commands):
            command_body += "".join([
                    command_template.format(prefix=prefix, command_name=command_.name.lower(), args=item.args,
                                            response=item.response
                                            ) for item in commands])

        if commands_admonitions:
            for admonition in commands_admonitions:
                if admonition.position == "bottom":
                    command_body += admonition_template.format(type=admonition.type, title=admonition.title,
                                                               message=admonition.message
                                                               )

        responses[lang][command_.name.lower()] = command_body

    return responses
