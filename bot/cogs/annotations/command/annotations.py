# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import commands, Context
from bot.models import Annotation
from bot.translations import Response

if TYPE_CHECKING:
    from bot.bot import Gorenmu


# TODO: Maybe add whisper annotations


class AnnotationsCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: Context) -> bool:  # NOQA
        return True

    @commands.base_decorator("Annotations")
    @commands.group(name="annotations", aliases=["note", "annotation"])
    async def annotations(self, ctx: Context) -> Response:  # NOQA
        await ctx.simple_response(ctx, "Shush")
        return ctx.user.translations.Admin.Nada.vazio.format_response(ctx, success=False)

    @commands.base_decorator("Annotations.Add")
    @annotations.command(name="add", aliases=[])
    async def add(self, ctx: Context, *, content: str = ""):
        translations = ctx.user.translations.Annotations
        if not content:
            return ctx.user.translations.Exceptions.no_content_provided.format_response(ctx, success=False)
        content, title = ctx.bot.StringTools.extract_and_remove_field(content, "title")
        if title and len(title) > 32:
            return translations.title_too_long.format_response(ctx, success=False)
        if len(content) > 450:
            return ctx.user.translations.Exceptions.too_much_characters.format_response(ctx, success=False)
        annotation = await Annotation.create(content=content, user=ctx.user, title=title)
        return translations.annotation_created.format_response(ctx, annotation.id)

    @commands.base_decorator("Annotations.Check")
    @annotations.command(name="check", aliases=[])
    async def check(self, ctx: Context, *, content: str = ""):
        translations = ctx.user.translations.Annotations
        if content and not content.isdigit():
            return ctx.user.translations.Exceptions.id_not_valid.format_response(ctx, content, success=False)
        if not content:
            annotation = await Annotation.filter(user=ctx.user, deleted=False)
            if not annotation:
                return translations.no_annotation_present.format_response(ctx, success=False)
            annotations_ = ", ".join([f'{note.title or ""} [{note.id}]' for note in annotation])
            return translations.all_annotations.format_response(ctx, annotations_)
        annotation = await Annotation.get_or_none(id=int(content), user=ctx.user, deleted=False)
        if not annotation:
            return translations.no_annotations_with_id.format_response(ctx, int(content), success=False)
        return translations.annotation_content.format_response(ctx, annotation.content)

    @commands.base_decorator("Annotations.Delete")
    @annotations.command(name="delete", aliases=[], pipeble=False)
    async def delete(self, ctx: Context, *, content: str = ""):
        if content.isdigit():
            annotation = await Annotation.get_or_none(id=int(content), user=ctx.user)
            translations = ctx.user.translations.Annotations
            if not annotation:
                return translations.no_annotations_with_id.format_response(ctx, int(content), success=False)
            annotation.deleted = True
            await annotation.save()
            return translations.deleted.format_response(ctx, annotation.id)
        return ctx.user.translations.Exceptions.no_id_provided.format_response(ctx, content)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(AnnotationsCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
