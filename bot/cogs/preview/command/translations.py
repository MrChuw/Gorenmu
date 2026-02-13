from __future__ import annotations

from typing import TYPE_CHECKING

import yarl

from bot.ext import Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .preview import PreviewCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: PreviewCmd) -> None:
        super().__init__(bot, __file__)
        self.parent: PreviewCmd = parent
        self.populate_subclasses(parent=self)

    class Preview(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Preview"

        def not_live(self, name: str) -> Response:
            text = self.get_text(self._cname, name=name)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def preview(self, preview_url: str, vod_url: yarl.URL) -> Response:
            text = self.get_text(self._cname, preview=preview_url, vod=vod_url.human_repr())
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        # region Hide.

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        # endregion

    Preview: Preview
