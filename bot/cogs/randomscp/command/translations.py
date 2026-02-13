from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import CommandExemples, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .randomscp import RandomScpCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: RandomScpCmd) -> None:
        super().__init__(bot, __file__)
        self.parent: RandomScpCmd = parent
        self.populate_subclasses(parent=self)

    class RandomScp(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "RandomScp"

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

    RandomScp: RandomScp
