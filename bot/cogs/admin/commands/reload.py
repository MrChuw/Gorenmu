# -*- coding: utf-8 -*-
from bot.ext.commands import base_decorator, Bucket, check, command, Context, cooldown, Command
from bot.translations import EnDecorators, Response
from bot.utils import Check, Role
from bot.bot import Gorenmu


@base_decorator(EnDecorators.Admin.Reload)
@cooldown(rate=3, per=10, bucket=Bucket.user)
@check([Role.dev])
@command(name='reload', aliases=[])
async def command(ctx: Context) -> Response:
    ctx.bot.CommandHandler.reload_cogs(ctx.bot)
    return ctx.translations.Admin.Reload().commands_reloaded.format_response(ctx)



def dynamic_description(command_: Command, bot: Gorenmu, ctx: Context = None, ) -> dict[str, dict[str, str]]:
    responses: dict[str, dict[str, str]] = {}
    cooldown_ = command_._cooldowns[0]  # NOQA
    per = cooldown_._per  # NOQA
    rate = cooldown_._rate  # NOQA
    prefix = ctx.prefix if ctx else bot.config.BotConfig.prefix[0]
    for lang in command_.decorators:
        if lang not in responses:
            responses[lang] = {}
        decorator: EnDecorators.Admin.Reload = command_.decorators[lang]
        description = decorator.get_description(decorator)  # NOQA
        base_decorators = bot.TranslationManager.get_decorator(lang)
        cooldown_type = base_decorators.get_bucket_type(cooldown_.bucket)
        afk_template = getattr(decorator, 'template', EnDecorators.Admin.Reload.template).format(
                rate=rate,
                per=per,
                cooldown_type=cooldown_type,
                description=description,
                command_title=command_.name.capitalize(),
                command_name=command_.name.lower(),
                prefix=prefix,
                aliases=", ".join([])
                )

        responses[lang][command_.name.lower()] = afk_template

    return responses
