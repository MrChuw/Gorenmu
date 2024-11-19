# -*- coding: utf-8 -*-
import datetime

from bot.bot import Gorenmu
from bot.ext.commands import base_decorator, Bucket, check, command, Command, Context, cooldown
from bot.translations import BaseDecorators, Response
from bot.utils import Role


@base_decorator(BaseDecorators.Admin.Nada)
@cooldown(rate=3, per=10, bucket=Bucket.user)
@check([Role.dev])
@command(name='nada', aliases=[])
async def command(ctx: Context, *, args, ) -> Response:
    translations = ctx.translations.Admin.Nada
    teste = datetime.datetime.now(datetime.timezone.utc)

    return translations.nada.format_response(ctx, args, success=True, handle=None, response_list=[])


# TODO: remover ele daqui e fazer genérico, e adicionar uma opção para templates como o do aliás que sempre
#  precisara ser um grande template ao inves de somente os comandos com descrição generica.
def dynamic_description(command_: Command, bot: Gorenmu, ctx: Context = None, ) -> dict[str, dict[str, str]]:
    responses: dict[str, dict[str, str]] = {}
    cooldown_ = command_._cooldowns[0]  # NOQA
    per = cooldown_._per  # NOQA
    rate = cooldown_._rate  # NOQA
    prefix = ctx.prefix if ctx else bot.config.BotConfig.prefix[0]
    for lang in command_.decorators:
        if lang not in responses:
            responses[lang] = {}
        decorator: BaseDecorators.Admin.Nada = command_.decorators[lang]
        description = decorator.get_description(decorator)  # NOQA
        base_decorators = bot.TranslationManager.get_decorator(lang)
        cooldown_type = base_decorators.get_bucket_type(cooldown_.bucket)

        language: BaseDecorators = bot.TranslationManager.languages[lang][0]
        command_body_template1: str = language.Templates.template_part1
        command_body_template2: str = language.Templates.template_part2
        command_body_template3: str = language.Templates.template_part3
        alias_template: str = language.Templates.alias_template
        command_template: str = language.Templates.command_template
        admonition_template: str = language.Templates.admonition_template

        aliases = ""
        if command_.aliases:
            aliases = alias_template.format(command_title=command_.name.capitalize(),
                                            aliases=", ".join(command_.aliases)
                                            )

        command_body = command_body_template1.format(command_title=command_.name.capitalize(), rate=rate, per=per,
                                                     cooldown_type=cooldown_type, )
        commands_admonitions = getattr(decorator, 'admonitions', BaseDecorators.Admin.Nada.admonitions)
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

        if commands := getattr(decorator, 'commands', BaseDecorators.Admin.Nada.commands):
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
