from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Admonitions, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .echo import EchoCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: EchoCmd) -> None:
        super().__init__(bot, __file__)
        self.parent: EchoCmd = parent
        self.populate_subclasses(parent=self)

    class Echo(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Echo"

        def echo(self, args) -> Response:
            text = self.get_text(self._cname, args=args)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_admonitions(self, *args, **kwargs) -> Admonitions:
            return Admonitions(
                [
                    {
                        "admonition_type": "warning",
                        "position": "top",
                        "title": self.get_text("adm_title"),
                        "message": self.get_text("adm_msg"),
                    }
                ]
            )

    Echo: Echo
