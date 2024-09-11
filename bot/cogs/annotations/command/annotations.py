# -*- coding: utf-8 -*-
import re

from bot.bot import Gorenmu
from bot.ext.commands import base_decorator, Bucket, check, command, Command, Context, cooldown
from bot.models.User_extras import Annotation
from bot.translations import EnDecorators, Response


@base_decorator(EnDecorators.Annotations)
@cooldown(rate=3, per=10, bucket=Bucket.user)
@check([])
@command(name='annotations', aliases=['note', 'annotation'])
async def command(ctx: Context, option="", *, content="") -> Response:
    if option in ['add']:
        return await add(ctx, content)
    elif option in ['check']:
        return await check(ctx, content)
    elif option in ['delete']:
        return await delete(ctx, content)
    else:
        return ctx.translations.Annotations.option_not_recognized.format_response(ctx)


async def add(ctx: Context, content: str) -> Response:
    translations = ctx.translations.Annotations
    title = None
    if match := re.search(r'title:"(.*?)"', content):
        title = match[1]
        content = content.replace(f'title:"{title}"', "")
    if len(title) > 32:
        return translations.title_too_long.format_response(ctx, False)
    if len(content) > 450:
        return translations.too_much_characters.format_response(ctx, success=False)
    if not content:
        return translations.too_few_characters.format_response(ctx, success=False)
    annotation = await Annotation.create(content=content, user=ctx.user, title=title)
    return translations.annotation_created.format_response(ctx, annotation.id)


async def check(ctx: Context, content: str) -> Response:
    translations = ctx.translations.Annotations
    if content.isdigit():
        annotation = await Annotation.get_or_none(id=int(content), user=ctx.user)
        if not annotation:
            return translations.no_annotations_with_id.format_response(ctx, int(content), success=False)
        return translations.annotation_content.format_response(ctx, annotation.content)
    annotation = await Annotation.create(content=content, user=ctx.user)
    annotations = ", ".join([f'{nota.title or ""} [{nota.id}]' for nota in annotation])
    return translations.all_annotations.format_response(ctx, annotations)


async def delete(ctx: Context, content: str) -> Response:
    translations = ctx.translations.Annotations
    if content.isdigit():
        annotation = await Annotation.get_or_none(id=int(content), user=ctx.user)
        if not annotation:
            return translations.no_annotations_with_id.format_response(ctx, int(content), success=False)
        annotation.deleted = True
        await annotation.save()
        return translations.deleted.format_response(ctx, annotation.id)

    return translations.id_not_provided.format_response(ctx, content)


def dynamic_description(command_: Command, bot: Gorenmu, ctx: Context = None, ) -> dict[str, dict[str, str]]:
    responses: dict[str, dict[str, str]] = {}
    cooldown_ = command_._cooldowns[0]  # NOQA
    per = cooldown_._per  # NOQA
    rate = cooldown_._rate  # NOQA
    prefix = ctx.prefix if ctx else bot.config.BotConfig.prefix[0]
    for lang in command_.decorators:
        if lang not in responses:
            responses[lang] = {}
        decorator: EnDecorators.Annotations = command_.decorators[lang]
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
        commands_admonitions = getattr(decorator, 'admonitions', EnDecorators.Annotations.admonitions)
        for admonition in commands_admonitions:
            if admonition.position == "top":
                command_body += admonition_template.format(type=admonition.type, title=admonition.title,
                                                           message=admonition.message
                                                           )

        command_body += command_body_template2.format(description=description, aliases=aliases)

        for admonition in commands_admonitions:
            if admonition.position == "middle":
                command_body += admonition_template.format(type=admonition.type, title=admonition.title,
                                                           message=admonition.message
                                                           )

        command_body += command_body_template3

        if commands := getattr(decorator, 'commands', EnDecorators.Annotations.commands):
            command_body += "".join([
                    command_template.format(prefix=prefix, command_name=command_.name.lower(), args=item.args,
                                            response=item.response
                                            ) for item in commands])

        for admonition in commands_admonitions:
            if admonition.position == "bottom":
                command_body += admonition_template.format(type=admonition.type, title=admonition.title,
                                                           message=admonition.message
                                                           )

        responses[lang][command_.name.lower()] = command_body

    return responses
