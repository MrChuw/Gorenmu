from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import CommandExemples, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .math import MathCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: MathCmd) -> None:
        super().__init__(bot, __file__)
        self.parent: MathCmd = parent
        self.populate_subclasses(parent=self)

    class Math(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Math"

        def not_supported(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

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
                    {"args": "1 + 1", "response": "2"},
                    {"args": "sqrt(523452)", "response": "723.4998272287285"},
                    {"args": "k = matrix(); k.subset(index(2), 6)", "response": "[[0, 6]]"},
                    {
                        "args": "h = diag(range(1, 4)); h.subset(index([1, 2], [1, 2]))",
                        "response": "[[[1, 0], [0, 2]]]",
                    },
                    {
                        "args": "diag(range(1, 4))",
                        "response": "[[1, 0, 0, 0], [0, 2, 0, 0], [0, 0, 3, 0], [0, 0, 0, 4]]",
                    },
                    {"args": "sum(range(10,20))", "response": "165"},
                ]
            )

        # endregion

    Math: Math
