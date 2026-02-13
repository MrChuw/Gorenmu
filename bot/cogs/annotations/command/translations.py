from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Admonitions, CommandExemples, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .annotations import AnnotationsCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: AnnotationsCmd) -> None:
        super().__init__(bot, __file__)
        self.parent: AnnotationsCmd = parent
        self.populate_subclasses(parent=self)

    class Add(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Add"

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text("deco_helper")

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text("deco_usage", prefix=prefix)

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text("deco_description")

        def deco_commands(self, *args, **kwargs) -> CommandExemples:
            return CommandExemples(
                [
                    {"args": self.get_text("cmd_ex1_args"), "response": self.get_text("cmd_ex1_res")},
                    {"args": self.get_text("cmd_ex2_args"), "response": self.get_text("cmd_ex2_res")},
                ]
            )

        def deco_admonitions(self, *args, **kwargs) -> Admonitions:
            p = kwargs.get("prefix", "!")
            return Admonitions(
                [
                    {
                        "admonition_type": "warning",
                        "position": "bottom",
                        "title": self.get_text("adm1_title"),
                        "message": self.get_text("adm1_msg"),
                    },
                    {
                        "admonition_type": "warning",
                        "position": "bottom",
                        "title": self.get_text("adm2_title"),
                        "message": self.get_text("adm2_msg"),
                    },
                    {
                        "admonition_type": "tip",
                        "position": "top",
                        "title": self.get_text("adm3_title"),
                        "message": self.get_text("adm3_msg", prefix=p),
                    },
                ]
            )

    Add: Add

    class Check(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Check"

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text("deco_helper")

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text("deco_usage", prefix=prefix)

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text("deco_description")

        def deco_commands(self, *args, **kwargs) -> CommandExemples:
            return CommandExemples(
                [
                    {"args": self.get_text("cmd_ex1_args"), "response": self.get_text("cmd_ex1_res")},
                    {"args": self.get_text("cmd_ex2_args"), "response": self.get_text("cmd_ex2_res")},
                ]
            )

    Check: Check

    class Delete(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Delete"

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text("deco_helper")

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text("deco_usage", prefix=prefix)

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text("deco_description")

        def deco_commands(self, *args, **kwargs) -> CommandExemples:
            return CommandExemples([{"args": self.get_text("cmd_ex1_args"), "response": self.get_text("cmd_ex1_res")}])

    Delete: Delete

    class Annotations(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Annotations"

        def title_too_long(self, *args) -> Response:
            text = self.get_text("title_too_long")
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def too_few_characters(self, *args) -> Response:
            text = self.get_text("too_few_characters")
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def annotation_created(self, note_id) -> Response:
            text = self.get_text("annotation_created", note_id=note_id)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def no_annotations_with_id(self, note_id) -> Response:
            text = self.get_text("no_annotations_with_id", note_id=note_id)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def all_annotations(self, note_id) -> Response:
            text = self.get_text("all_annotations", note_id=note_id)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def annotation_content(self, content) -> Response:
            text = self.get_text("annotation_content", content=content)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def deleted(self, note_id) -> Response:
            text = self.get_text("deleted", note_id=note_id)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def option_not_recognized(self) -> Response:
            text = self.get_text("option_not_recognized")
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def no_annotation_present(self) -> Response:
            text = self.get_text("no_annotation_present")
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text("deco_helper")

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text("deco_usage", prefix=prefix)

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text("deco_description")

    Annotations: Annotations
