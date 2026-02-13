from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import CommandExemples, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .chance import ChanceCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: ChanceCmd) -> None:
        super().__init__(bot, __file__)
        self.parent: ChanceCmd = parent
        self.populate_subclasses(parent=self)

    class Chance(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Chance"

        def response(self, value: int | str) -> Response:
            text = self.get_text(self._cname, value=value)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_commands(self, *args, **kwargs) -> CommandExemples:
            return CommandExemples([{"response": self.get_text("cmd_ex1_res")}])

    Chance: Chance
