from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import CommandExemples, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.ext import Context


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu) -> None:
        super().__init__(bot)
        self.populate_subclasses()

    class Math(TBase):
        def __init__(self):
            super().__init__()

        def not_supported(self, ctx: Context) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    'The use of "math." or "mathjs." is not supported, use only "pi" or "e" instead of math.pi/math.e.',
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    'Uso de "math." ou "mathjs." não é suportado, use somente "pi" ou "e" ao em vez de math.pi/math.e',
                )
            return response.format_response(self._untangle_str(ctx, self._cname), ctx.bot.dev_user.display_name)

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    "Enter the command and a mathematical operation for me to solve it.",
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Digite o comando e uma operação matemática para eu resolvê-la.",
                )
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "To use: {}math (mathematical expression)")
                self.lang_dict.add_with(["pt_br", "pt"], "Para usar: {}math (expressão matemática)")
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    "Enter the command and a mathematical operation for me to solve it.",
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Digite o comando e uma operação matemática para eu resolvê-la.",
                )
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    ["pt_br", "pt", "en"],
                    CommandExemples(
                        [
                            {"args": "1 + 1", "response": "2"},
                            {"args": "sqrt(523452)", "response": "723.4998272287285"},
                            {
                                "args": "k = matrix(); k.subset(index(2), 6)",
                                "response": "[[0, 6]]",
                            },
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
                    ),
                )
            return self._untangle_commands(ctx, self._cname)

        # endregion

    Math: Math
