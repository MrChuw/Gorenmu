from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import CommandExemples, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .upsidedown import UpSideDownCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: UpSideDownCmd) -> None:
        super().__init__(bot, __file__)
        self.parent: UpSideDownCmd = parent
        self.populate_subclasses(parent=self)

    class UpSideDown(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "UpSideDown"

        def upsidedown(self, text: str) -> Response:
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
            return CommandExemples([{"args": "tests", "response": self.get_text("cmd_res")}])

        # endregion

    UpSideDown: UpSideDown
