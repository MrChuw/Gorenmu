# -*- coding: utf-8 -*-
from bot.ext.commands import Bucket, check, Context, cooldown, base_decorator, helper, usage, command
from bot.translations import EnDecorators, Response
from bot.bot import Gorenmu
from bot.ext.commands import Command
from bot.apis.upsidedown import transform


@base_decorator(EnDecorators.UpSideDown)
@cooldown(rate=3, per=10, bucket=Bucket.user)
@check([])
@command(name='upsidedown', aliases=['updown'])
async def command(ctx: Context, *, content, ) -> Response:
    return ctx.translations.UpSideDown.upsidedown.format_response(ctx, transform(content))


def dynamic_description(command_: Command, bot: Gorenmu, ctx: Context = None, ) -> dict[str, dict[str, str]]:
    responses: dict[str, dict[str, str]] = {}
    cooldown_ = command_._cooldowns[0]  # NOQA
    per = cooldown_._per  # NOQA
    rate = cooldown_._rate  # NOQA
    prefix = ctx.prefix if ctx else bot.config.BotConfig.prefix[0]
    for lang in command_.decorators:
        if lang not in responses:
            responses[lang] = {}
        decorator: EnDecorators.UpSideDown = command_.decorators[lang]
        description = decorator.get_description(decorator)  # NOQA
        base_decorators = bot.TranslationManager.get_decorator(lang)
        cooldown_type = base_decorators.get_bucket_type(cooldown_.bucket)
        afk_template = getattr(decorator, 'template', EnDecorators.UpSideDown.template).format(
                rate=rate,
                per=per,
                cooldown_type=cooldown_type,
                description=description,
                command_title=command_.name.capitalize(),
                command_name=command_.name.lower(),
                prefix=prefix,
                aliases=", ".join(command_.aliases)
                )

        responses[lang][command_.name.lower()] = afk_template

    return responses

