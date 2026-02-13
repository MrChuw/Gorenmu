from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import CommandExemples, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .accountage import AccountAgeCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: AccountAgeCmd) -> None:
        super().__init__(bot, __file__)
        self.parent: AccountAgeCmd = parent
        self.populate_subclasses(parent=self)

    class AccountAge(TBase):
        def __init__(self, parent):
            super().__init__(parent)
            self.prefix = "AccountAge"

        def accountage(self, mention: str, date: str, delta: str):
            text = self.get_text(self._cname, mention=mention, date=date, delta=delta)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        accountage: Response = accountage

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_commands(self, *args, **kwargs) -> CommandExemples:
            return CommandExemples(
                [
                    {"args": self.get_text("cmd_ex1_args"), "response": self.get_text("cmd_ex1_res")},
                    {"args": self.get_text("cmd_ex2_args"), "response": self.get_text("cmd_ex2_res")},
                ]
            )

    AccountAge: AccountAge
