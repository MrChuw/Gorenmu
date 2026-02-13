from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .bug import BugCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: BugCmd) -> None:
        super().__init__(bot, __file__)
        self.parent: BugCmd = parent
        self.populate_subclasses(parent=self)

    class Bug(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Bug"

        def bug(self, bug_id: str | int) -> Response:
            text = self.get_text(self._cname, bug_id=bug_id)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

    Bug: Bug
