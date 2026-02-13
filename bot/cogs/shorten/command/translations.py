from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .shorten import ShortenCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: ShortenCmd) -> None:
        super().__init__(bot, __file__)
        self.parent: ShortenCmd = parent
        self.populate_subclasses(parent=self)

    class Shorten(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Shorten"

        def api_erro(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def urls(self, urls: str) -> Response:
            text = self.get_text(self._cname, urls=urls)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def url(self, url: str) -> Response:
            text = self.get_text(self._cname, url=url)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

    Shorten: Shorten
