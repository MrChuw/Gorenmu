from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import CommandExemples, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .randomscp import RandomSCPCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: RandomSCPCmd) -> None:
        super().__init__(bot=bot, file=__file__, upper=parent)
        self.RandomScp: RandomScp = RandomScp(self)


class RandomScp(TBase):
    def __init__(self, parent: Translations):
        self.prefix = "RandomScp"
        super().__init__(parent, __file__)

    def deco_helper(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)

    def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
        return self.get_text(self._cname, prefix=prefix)

    def deco_description(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)

    def deco_commands(self, *args, **kwargs) -> CommandExemples:
        return CommandExemples([{"response": self.get_text("cmd_res")}])

