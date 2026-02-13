from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .leave import LeaveCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: LeaveCmd) -> None:
        super().__init__(bot, __file__)
        self.parent: LeaveCmd = parent
        self.populate_subclasses(parent=self)

    class Leave(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Leave"

        def not_on_channel(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def channel_removed(self, args: str) -> Response:
            text = self.get_text(self._cname, args=args)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        # region Hide.

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        # endregion

    Leave: Leave
