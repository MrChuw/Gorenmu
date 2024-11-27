# -*- coding: utf-8 -*-
import re

from bot.bot import Gorenmu
from bot.ext.commands import base_decorator, Bucket, check, command, Command, Context, cooldown
from bot.models.User_extras import Annotation
from bot.translations import BaseDecorators, Response


@base_decorator(BaseDecorators.Annotations)
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
    title = ""
    if match := re.search(r'title:"(.*?)"', ctx.message.content):
        title = match[1]
        content = content.replace(title, "")
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
    annotation = await Annotation.filter(user=ctx.user, deleted=False)
    annotations = ", ".join([f'{note.title or ""} [{note.id}]' for note in annotation])
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


