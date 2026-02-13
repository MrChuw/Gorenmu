from __future__ import annotations

from typing import TYPE_CHECKING

import yarl

from bot.ext import CommandExemples, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .randomcolor import RandomColorCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: RandomColorCmd) -> None:
        super().__init__(bot, __file__)
        self.parent: RandomColorCmd = parent
        self.populate_subclasses(parent=self)

    class RandomColor(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "RandomColor"

        def api_down(self) -> str:
            return self.get_text(self._cname)

        def response_url(self, hex_code: str, name: str, url: yarl.URL) -> Response:
            text = self.get_text(self._cname, hex_code=hex_code, name=name, url=url.human_repr())
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        # region Hide.

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_commands(self, *args, **kwargs) -> CommandExemples:
            return CommandExemples([{"response": self.get_text("cmd_res")}])

        # endregion

    RandomColor: RandomColor
