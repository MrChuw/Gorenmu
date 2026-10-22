from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import CommandExemples, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .math import MathCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: MathCmd) -> None:
        super().__init__(bot=bot, file=__file__, upper=parent)
        self.Math: Math = Math(self)


class Math(TBase):
    def __init__(self, parent: Translations):
        self.prefix = "Math"
        super().__init__(parent, __file__)

    def not_supported(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def too_much_memory(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def undefined_symbol(self, symbol: str) -> Response:
        text = self.get_text(self._cname, symbol=symbol)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def invalid_expression(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=False, response=text)


    def evaluation_timeout(self, timeout: int) -> Response:
        text = self.get_text(self._cname, timeout=timeout)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def expression_too_complex(self, limit: int) -> Response:
        text = self.get_text(self._cname, limit=limit)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def result_too_large(self, error: str) -> Response:
        text = self.get_text(self._cname, error=error)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def operation_not_supported(self, operation: str) -> Response:
        text = self.get_text(self._cname, operation=operation)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def invalid_value(self, message: str) -> Response:
        text = self.get_text(self._cname, message=message)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def matrix_error(self, message: str) -> Response:
        text = self.get_text(self._cname, message=message)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def incompatible_units(self, message: str) -> Response:
        text = self.get_text(self._cname, message=message)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def unknown_unit(self, message: str) -> Response:
        text = self.get_text(self._cname, message=message)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def polynomial_error(self, message: str) -> Response:
        text = self.get_text(self._cname, message=message)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def index_out_of_range(self, message: str) -> Response:
        text = self.get_text(self._cname, message=message)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def value_error(self, error: str) -> Response:
        text = self.get_text(self._cname, error=error)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def memory_limit_exceeded(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=False, response=text)


    def deco_helper(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)

    def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
        return self.get_text(self._cname, prefix=prefix)


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

