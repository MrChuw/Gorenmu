# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Context, Response, commands
from bot.models import Annotation
from bot.utils import StringTools

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


# TODO: Maybe add whisper annotations


class AnnotationsCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.StringTools: StringTools = StringTools()
        self.translations: Translations = Translations(bot)

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: Context) -> bool:  # NOQA
        return True

    @commands.group(name="annotations", aliases=["note", "annotation"])
    async def annotations(self, ctx: Context) -> Response:  # NOQA
        await ctx.simple_response(ctx, "Shush")
        return self.translations.Exceptions.empty(ctx)

    @annotations.command(name="add", aliases=[])
    async def add(self, ctx: Context, *, content: str = ""):
        translations = self.translations.Annotations
        if not content:
            return self.translations.Exceptions.no_content_provided(ctx)
        content, title = self.StringTools.extract_and_remove_field(content, "title")
        if title and len(title) > 32:
            return translations.title_too_long(ctx)
        if len(content) > 450:
            return self.translations.Exceptions.too_much_characters(ctx)
        annotation = await Annotation.create(content=content, user=ctx.user, title=title)
        return translations.annotation_created(ctx, annotation.id)

    @annotations.command(name="check", aliases=[])
    async def check(self, ctx: Context, *, content: str = ""):
        translations = self.translations.Annotations
        if content and not content.isdigit():
            return self.translations.Exceptions.id_not_valid(ctx, content)
        if not content:
            annotation = await Annotation.filter(user=ctx.user)
            if not annotation:
                return translations.no_annotation_present(ctx)
            annotations_ = ", ".join([f'{note.title or ""} [{note.id}]' for note in annotation])
            return translations.all_annotations(ctx, annotations_)
        annotation = await Annotation.get_or_none(id=int(content), user=ctx.user, deleted=False)
        if not annotation:
            return translations.no_annotations_with_id(ctx, int(content))
        return translations.annotation_content(ctx, annotation.content)

    @annotations.command(name="delete", aliases=[], pipeble=False)
    async def delete(self, ctx: Context, *, content: str = ""):
        if content.isdigit():
            annotation = await Annotation.get_or_none(id=int(content), user=ctx.user)
            translations = self.translations.Annotations
            if not annotation:
                return translations.no_annotations_with_id(ctx, int(content))
            annotation.deleted = True
            await annotation.save()
            return translations.deleted(ctx, annotation.id)
        return self.translations.Exceptions.no_id_provided(ctx)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(AnnotationsCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
