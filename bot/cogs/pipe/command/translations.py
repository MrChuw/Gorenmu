from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Admonitions, CommandExemples, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .pipe import PipeCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: PipeCmd) -> None:
        super().__init__(bot, __file__)
        self.parent: PipeCmd = parent
        self.populate_subclasses(parent=self)

    class Pipe(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Pipe"

        def pipe(self, link: str) -> Response:
            text = self.get_text(self._cname, link=link)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        # region Hide.

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_commands(self, *args, **kwargs) -> CommandExemples:
            prefix = self.ctx_get().prefix
            return CommandExemples(
                [{"args": self.get_text("cmd_ex1", prefix=prefix)}, {"args": self.get_text("cmd_ex2", prefix=prefix)}]
            )

        def deco_admonitions(self, *args, **kwargs) -> Admonitions:
            return Admonitions(
                [
                    {
                        "admonition_type": "warning",
                        "position": "top",
                        "title": self.get_text("adm_cool_title"),
                        "message": self.get_text("adm_cool_msg"),
                    },
                    {
                        "admonition_type": "info",
                        "position": "bottom",
                        "title": self.get_text("adm_info_title"),
                        "message": self.get_text("adm_info_msg"),
                    },
                    {
                        "admonition_type": "info",
                        "position": "bottom",
                        "title": self.get_text("adm_work_title"),
                        "message": self.get_text("adm_work_msg"),
                    },
                ]
            )

        # endregion

    Pipe: Pipe
