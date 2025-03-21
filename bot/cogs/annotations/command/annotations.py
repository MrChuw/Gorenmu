# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import TYPE_CHECKING
import re

from bot.ext import commands, Context
from bot.models import Annotation
from bot.translations import BaseDecorators, Response


if TYPE_CHECKING:
    from bot.bot import Gorenmu

__all__ = 'AnnotationsCmd'
# TODO: Maybe add whisper annotations


class AnnotationsCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None:
        ...

    @commands.Component.guard()
    def guards_component(self, ctx: commands.Context) -> bool:
        return True

    @commands.base_decorator(BaseDecorators.Annotations)
    @commands.group(name='annotations', aliases=['note', 'annotation'])
    async def annotations(self, ctx: Context, *, content="") -> Response:
        await ctx.simple_response(ctx, "Shush")  # Dont know what to put here
        return ctx.user.translations.Admin.Nada.vazio.format_response(ctx, success=False)

    @annotations.command(name="add", aliases=[])
    async def add(self, ctx: Context, *, content: str = ""):
        translations = ctx.user.translations.Annotations
        content, title = ctx.bot.ToolsTools.extract_and_remove_field(content, "title")
        if len(title) > 32:
            return translations.title_too_long.format_response(ctx, success=False)
        if len(content) > 450:
            return ctx.user.translations.Exceptions.too_much_characters.format_response(ctx, success=False)
        if not content:
            return translations.too_few_characters.format_response(ctx, success=False)
        annotation = await Annotation.create(content=content, user=ctx.user, title=title)
        return translations.annotation_created.format_response(ctx, annotation.id)

    @annotations.command(name="check", aliases=[])
    async def check(self, ctx: Context, *, content: str = ""):
        translations = ctx.user.translations.Annotations
        if content.isdigit():
            annotation = await Annotation.get_or_none(id=int(content), user=ctx.user)
            if not annotation:
                return translations.no_annotations_with_id.format_response(ctx, int(content), success=False)
            return translations.annotation_content.format_response(ctx, annotation.content)
        annotation = await Annotation.filter(user=ctx.user, deleted=False)
        annotations_ = ", ".join([f'{note.title or ""} [{note.id}]' for note in annotation])
        return translations.all_annotations.format_response(ctx, annotations_)

    @annotations.command(name="delete", aliases=[])
    async def delete(self, ctx: Context, *, content: str = ""):
        translations = ctx.user.translations.Annotations
        if content.isdigit():
            annotation = await Annotation.get_or_none(id=int(content), user=ctx.user)
            if not annotation:
                return translations.no_annotations_with_id.format_response(ctx, int(content), success=False)
            annotation.deleted = True
            await annotation.save()
            return translations.deleted.format_response(ctx, annotation.id)
        return translations.id_not_provided.format_response(ctx, content)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(AnnotationsCmd(bot))


async def teardown(bot: Gorenmu) -> None:
    ...
