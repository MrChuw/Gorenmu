# -*- coding: utf-8 -*-
import re
import string

from urlextract import URLExtract

from bot.bot import Gorenmu
from bot.ext.commands import base_decorator, Bucket, check, command, Command, Context, cooldown
from bot.translations import EnDecorators, Response


@base_decorator(EnDecorators.Count)
@cooldown(rate=3, per=10, bucket=Bucket.user)
@check([])
@command(name='count', aliases=[])
async def command(ctx: Context, *, content: str) -> Response:
    if (urls := URLExtract().find_urls(text=content)) and 'type:url' in content:
        content = ""
        cache_session = ctx.bot.SessionsCaches.CountCachedSession
        for url in urls:
            teste = await cache_session.session.get(url)
            content += f"{await teste.text()} "
    uppercase_count = len(re.findall(r'[A-Z]', content))
    punctuations_count = len(re.findall(f'[{re.escape(string.punctuation)}]', content))
    special_chars_count = len([char for char in re.findall(r'[^\w\s]', content) if char not in string.punctuation])
    return ctx.translations.Count.character_count.format_response(ctx, len(content), punctuations_count,
                                                                  uppercase_count, special_chars_count
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
        decorator: EnDecorators.Count = command_.decorators[lang]
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
                                            aliases=", ".join(command_.aliases)
                                            )

        command_body = command_body_template.format(command_title=command_.name.capitalize(), rate=rate, per=per,
                                                    description=description, cooldown_type=cooldown_type,
                                                    aliases=aliases
                                                    )

        command_responses = ""
        if commands := getattr(decorator, 'commands', EnDecorators.Count.commands):
            command_responses = "".join([
                    command_template.format(prefix=prefix, command_name=command_.name.lower(), args=item.args,
                                            response=item.response
                                            ) for item in commands])

        admonitions = ""
        if commands_admonitions := getattr(decorator, 'admonitions', EnDecorators.Count.admonitions):
            admonitions = "".join([admonition_template.format(type=admonition.type, title=admonition.title,
                                                              message=admonition.message, ) for admonition in
                                   commands_admonitions]
                                  )

        responses[lang][command_.name.lower()] = command_body + command_responses + admonitions

    return responses
