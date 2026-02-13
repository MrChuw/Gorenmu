from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import CommandExemples, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .count import CountCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: CountCmd) -> None:
        super().__init__(bot, __file__)
        self.parent: CountCmd = parent
        self.populate_subclasses(parent=self)

    class Count(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Count"

        def character_count(self, length, punc, upper, special) -> Response:
            text = self.get_text(self._cname, length=length, punc=punc, upper=upper, special=special)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        # region Hide.

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_commands(self, *args, **kwargs) -> CommandExemples:
            return CommandExemples(
                [
                    {
                        "prefix": self.get_text("cmd_ex1_prefix"),
                        "args": "some nice text! with some 😄 caracteres, spacial!",
                        "response": self.get_text("cmd_ex1_res"),
                    },
                    {
                        "prefix": self.get_text("cmd_ex2_prefix"),
                        "args": "https://example.org/",
                        "response": self.get_text("cmd_ex2_res"),
                    },
                    {
                        "prefix": self.get_text("cmd_ex3_prefix"),
                        "args": "type:url https://example.com/",
                        "response": self.get_text("cmd_ex3_res"),
                    },
                ]
            )

    # endregion

    Count: Count
