from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Admonitions, CommandExemples, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .safebooru import SafebooruCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: SafebooruCmd) -> None:
        super().__init__(bot, __file__)
        self.parent: SafebooruCmd = parent
        self.populate_subclasses(parent=self)

    class Safebooru(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Safebooru"

        def original(self) -> str:
            return self.get_text(self._cname)

        def preview(self) -> str:
            return self.get_text(self._cname)

        def too_much_tags(self, limit: int | str) -> Response:
            text = self.get_text(self._cname, limit=str(limit))
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def success(self, content: str) -> Response:
            text = self.get_text(self._cname, content=content)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        # region Hide.

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_commands(self, *args, **kwargs) -> CommandExemples:
            return CommandExemples(
                [
                    {"response": self.get_text("cmd_res")},
                    {
                        "args": "some_tag",
                        "response": self.get_text("cmd_res"),
                    },
                ]
            )

        def deco_admonitions(self, *args, **kwargs) -> Admonitions:
            return Admonitions(
                [
                    {
                        "admonition_type": "warning",
                        "position": "top",
                        "title": self.get_text("adm_tags_title"),
                        "message": self.get_text("adm_tags_msg"),
                    }
                ]
            )

        # endregion

    Safebooru: Safebooru
