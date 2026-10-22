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
        self.translations: Translations = Translations(bot, self)


    @commands.group(name="annotations", aliases=["note", "annotation"])
    async def annotations(self, ctx: Context) -> Response:
        await ctx.simple_response(ctx, "Shush")
        return self.translations.Exceptions.empty(ctx)

    @annotations.command(name="add", aliases=[])
    async def add(self, ctx: Context, *, content: str = ""):
        translations = self.translations.Annotations
        if not content:
            return self.translations.Exceptions.no_content_provided()
        content, title = self.StringTools.extract_and_remove_field(content, "title")
        if title and len(title) > 32:
            return translations.title_too_long()
        if len(content) > 450:
            return self.translations.Exceptions.too_much_characters()
        annotation = await Annotation.create(content=content, user=ctx.user, title=title)
        return translations.annotation_created(annotation.id)

    @annotations.command(name="check", aliases=[])
    async def check(self, ctx: Context, *, content: str = ""):
        translations = self.translations.Annotations
        if content and not content.isdigit():
            return self.translations.Exceptions.id_not_valid(content)
        if not content:
            annotation = await Annotation.filter(user=ctx.user)
            if not annotation:
                return translations.no_annotation_present()
            annotations_ = ", ".join([f'{note.title or ""} [{note.id}]' for note in annotation])
            return translations.all_annotations(annotations_)
        annotation = await Annotation.get_or_none(id=int(content), user=ctx.user, deleted=False)
        if not annotation:
            return translations.no_annotations_with_id(int(content))
        return translations.annotation_content(annotation.content)

    @annotations.command(name="delete", aliases=[], pipeble=False)
    async def delete(self, ctx: Context, *, content: str = ""):
        if content.isdigit():
            annotation = await Annotation.get_or_none(id=int(content), user=ctx.user)
            translations = self.translations.Annotations
            if not annotation:
                return translations.no_annotations_with_id(int(content))
            annotation.deleted = True
            await annotation.save()
            return translations.deleted(annotation.id)
        return self.translations.Exceptions.no_id_provided()


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(AnnotationsCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
