from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .nicks import NicksCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: NicksCmd) -> None:
        super().__init__(bot, __file__)
        self.parent: NicksCmd = parent
        self.populate_subclasses(parent=self)

    class Nicks(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Nicks"

        def not_seen(self, name: str) -> Response:
            text = self.get_text(self._cname, name=name)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        # region Hide.

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        # endregion

    Nicks: Nicks
