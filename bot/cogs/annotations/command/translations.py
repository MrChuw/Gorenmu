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
        self.Add: Add = Add(parent=self)
        self.Check: Check = Check(parent=self)
        self.Delete: Delete = Delete(parent=self)
        self.Annotations: Annotations = Annotations(parent=self)


class Add(TBase):
    def __init__(self, parent: Translations):
        self.prefix = "Anno-Add"
        super().__init__(parent, __file__)

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


class Check(TBase):
    def __init__(self, parent: Translations):
        self.prefix = "Anno-Check"
        super().__init__(parent, __file__)

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


class Delete(TBase):
    def __init__(self, parent: Translations):
        self.prefix = "Anno-Delete"
        super().__init__(parent, __file__)

    def deco_helper(self, *args, **kwargs) -> str:
        return self.get_text("deco_helper")

    def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
        return self.get_text("deco_usage", prefix=prefix)

    def deco_description(self, *args, **kwargs) -> str:
        return self.get_text("deco_description")

    def deco_commands(self, *args, **kwargs) -> CommandExemples:
        return CommandExemples([{"args": self.get_text("cmd_ex1_args"), "response": self.get_text("cmd_ex1_res")}])


class Annotations(TBase):
    def __init__(self, parent: Translations):
        self.prefix = "Annotations"
        super().__init__(parent, __file__)

    def title_too_long(self) -> Response:
        text = self.get_text("title_too_long")
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def too_few_characters(self) -> Response:
        text = self.get_text("too_few_characters")
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def annotation_created(self, note_id) -> Response:
        text = self.get_text("annotation_created", note_id=note_id)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def no_annotations_with_id(self, note_id) -> Response:
        text = self.get_text("no_annotations_with_id", note_id=note_id)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def all_annotations(self, note_id) -> Response:
        text = self.get_text("all_annotations", note_id=note_id)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def annotation_content(self, content) -> Response:
        text = self.get_text("annotation_content", content=content)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def deleted(self, note_id) -> Response:
        text = self.get_text("deleted", note_id=note_id)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def option_not_recognized(self) -> Response:
        text = self.get_text("option_not_recognized")
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def no_annotation_present(self) -> Response:
        text = self.get_text("no_annotation_present")
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def deco_helper(self, *args, **kwargs) -> str:
        return self.get_text("deco_helper")

    def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
        return self.get_text("deco_usage", prefix=prefix)

    def deco_description(self, *args, **kwargs) -> str:
        return self.get_text("deco_description")

