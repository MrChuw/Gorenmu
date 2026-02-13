from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .suggest import SuggestCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: SuggestCmd) -> None:
        super().__init__(bot, __file__)
        self.parent: SuggestCmd = parent
        self.populate_subclasses(parent=self)

    class Suggest(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Suggest"

        def suggest(self, id: int | str) -> Response:
            text = self.get_text(self._cname, id=str(id))
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        # region Hide.

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        # endregion

    Suggest: Suggest
