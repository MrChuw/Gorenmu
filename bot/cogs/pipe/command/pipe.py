# -*- coding: utf-8 -*-
import re

from bot.bot import Gorenmu
from bot.ext.commands import base_decorator, Bucket, check, command, Command, Context, cooldown
from bot.translations import EnDecorators, Response


@base_decorator(EnDecorators.Others.Pipe)
@cooldown(rate=3, per=10, bucket=Bucket.user)
@check([])
@command(name='pipe', aliases=[])
async def command(ctx: Context) -> Response:
    if ctx.user.language == ctx.bot.TranslationManager.languages[0]:
        url = f"{ctx.bot.config.BotConfig.site_url}{ctx.bot.TranslationManager.languages[0]}/commands/pipe.html"
    elif ctx.user.language == ctx.bot.TranslationManager.languages[1]:
        url = f"{ctx.bot.config.BotConfig.site_url}{ctx.bot.TranslationManager.languages[1]}/comandos/pipe.html"

    else:
        url = f"{ctx.bot.config.BotConfig.site_url}{ctx.bot.TranslationManager.languages[0]}/commands/pipe.html"
    return ctx.translations.Others.Pipe.response.format_response(ctx, url)


def dynamic_description(command_: Command, bot: Gorenmu, ctx: Context = None, ) -> dict[str, dict[str, str]]:
    responses: dict[str, dict[str, str]] = {}
    cooldown_ = command_._cooldowns[0]  # NOQA
    per = cooldown_._per  # NOQA
    rate = cooldown_._rate  # NOQA
    prefix = ctx.prefix if ctx else bot.config.BotConfig.prefix[0]
    for lang in command_.decorators:
        if lang not in responses:
            responses[lang] = {}
        decorator: EnDecorators.Others.Pipe = command_.decorators[lang]
        description = decorator.get_description(decorator)  # NOQA
        base_decorators = bot.TranslationManager.get_decorator(lang)
        cooldown_type = base_decorators.get_bucket_type(cooldown_.bucket)
        template = custom_format(getattr(decorator, 'template', EnDecorators.Alias.template),
                                 rate=rate,
                                 per=per,
                                 cooldown_type=cooldown_type,
                                 description=description,
                                 command_title=command_.name.capitalize(),
                                 command_name=command_.name.lower(),
                                 prefix=prefix,
                                 aliases=", ".join(command_.aliases)
                                 )

        responses[lang][command_.name.lower()] = template
    return responses


def custom_format(template, **kwargs):
    # Expressão regular para identificar apenas os placeholders que você deseja substituir
    pattern = re.compile(r"\{(rate|per|cooldown_type|description|command_title|command_name|prefix|aliases)}")

    # Função para substituir apenas os placeholders definidos em kwargs
    def replace(match):
        placeholder = match.group(1)
        return str(kwargs.get(placeholder, match.group(0)))

    # Substituir apenas os placeholders definidos em pattern
    return pattern.sub(replace, template)
