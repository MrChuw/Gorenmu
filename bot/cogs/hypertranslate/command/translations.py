from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import CommandExemples, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .hypertranslate import HyperTranslateCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: HyperTranslateCmd) -> None:
        super().__init__(bot, __file__)
        self.parent: HyperTranslateCmd = parent
        self.populate_subclasses(parent=self)

    class HyperTranslate(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "HyperTranslate"

        def base_lang(self) -> str:
            return self.get_text(self._cname)

        def starter_string(self) -> str:
            return self.get_text(self._cname)

        def unexpected_error(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def translation(self, text) -> Response:
            res_text = self.get_text(self._cname, text=text)
            return Response(ctx=self.ctx_get(), success=True, response_string=res_text)

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
                    {
                        "prefix": self.get_text("cmd_ex1_prefix"),
                        "args": self.get_text("cmd_ex1_args"),
                        "response": self.get_text("cmd_ex1_res"),
                    }
                ]
            )

        # endregion

    HyperTranslate: HyperTranslate
