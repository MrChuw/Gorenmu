from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .nicks import NicksCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: NicksCmd) -> None:
        super().__init__(bot=bot, file=__file__, upper=parent)
        self.Nicks: Nicks = Nicks(self)


class Nicks(TBase):
    def __init__(self, parent: Translations):
        self.prefix = "Nicks"
        super().__init__(parent, __file__)

    def not_seen(self, name: str) -> Response:
        text = self.get_text(self._cname, name=name)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def deco_helper(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)

    def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
        return self.get_text(self._cname, prefix=prefix)

    def deco_description(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)
