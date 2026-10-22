import math
from decimal import Decimal, getcontext
from typing import Any

import numpy as np

from .format_options import FormatOptions
from .formatter import format_value
from .mathjs_core import MathjsCore, _bell_numbers, _catalan
from .matrix import Index, Matrix, index
from .unit import Unit

getcontext().prec = 64


class Mathjs(MathjsCore):
    def __init__(
        self,
        precision: int = 64,
        max_depth: int = 50,
        max_digits: int = 100_000,
        timeout_seconds: float | None = None,
        max_memory_mb: int | None = None,
    ) -> None:
        super().__init__(
            precision=precision,
            max_depth=max_depth,
            max_digits=max_digits,
            timeout_seconds=timeout_seconds,
            max_memory_mb=max_memory_mb,
        )
        getcontext().prec = precision
        self._init_builtins()

    def evaluate(self, expr: str, scope: dict | None = None) -> Any:
        if scope:
            local_scope = self.scope.copy()
            local_scope.update(scope)
        else:
            local_scope = self.scope.copy()  # noqa

        with self._time_limit(self.timeout_seconds):
            return self._evaluate_statements(expr, local_scope)

    def _evaluate_statements(self, expr: str, local_scope: dict) -> Any:
        statements = self._split_statements(expr)
        result = None
        for stmt in statements:
            stmt = stmt.strip()
            if not stmt:
                continue
            py_stmt = self._transform(stmt)
            result = self._exec_stmt(py_stmt, local_scope)

        return result

    @staticmethod
    def format(value: Any, options: FormatOptions | None = None) -> str:
        return format_value(value, options)

    def _bignumber(self, value: Any) -> Any:
        if isinstance(value, str):
            evaluated = self.evaluate(value)
            return self._bignumber(evaluated)

        if isinstance(value, Decimal):
            return value

        if isinstance(value, Matrix):
            return value.map(lambda x: Decimal(str(x)))
        if isinstance(value, (list, tuple)):
            return [self._bignumber(item) for item in value]

        return Decimal(str(value))

    def _init_builtins(self) -> None:
        self.scope.update(
            {
                "pi": math.pi,
                "e": math.e,
                "tau": 2 * math.pi,
                "i": 1j,
                "true": True,
                "false": False,
                "null": None,
                "undefined": None,
                "Infinity": float("inf"),
                "NaN": float("nan"),
                "LN2": math.log(2),
                "LN10": math.log(10),
                "LOG2E": math.log2(math.e),
                "LOG10E": math.log10(math.e),
                "SQRT1_2": math.sqrt(0.5),
                "SQRT2": math.sqrt(2),
                "phi": (1 + math.sqrt(5)) / 2,
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "asin": math.asin,
                "acos": math.acos,
                "atan": math.atan,
                "atan2": math.atan2,
                "sinh": math.sinh,
                "cosh": math.cosh,
                "tanh": math.tanh,
                "asinh": math.asinh,
                "acosh": math.acosh,
                "atanh": math.atanh,
                "log": math.log,
                "log10": math.log10,
                "log2": math.log2,
                "exp": math.exp,
                "sqrt": math.sqrt,
                "abs": abs,
                "round": round,
                "floor": math.floor,
                "ceil": math.ceil,
                "sign": lambda x: (x > 0) - (x < 0),
                "factorial": self._safe_factorial,
                "combinations": math.comb,
                "permutations": lambda n, k=None: (
                    math.perm(n, k) if k is not None else math.factorial(n)
                ),
                "sum": self._sum,
                "mean": self._mean,
                "median": self._median,
                "std": self._std,
                "variance": self._variance,
                "prod": self._prod,
                "Matrix": Matrix,
                "det": self._det,
                "inv": self._inv,
                "matrix": Matrix,
                "transpose": self._transpose,
                "size": self._size,
                "norm": self._norm,
                "dot": self._dot,
                "cross": self._cross,
                "kron": self._kron,
                "ones": self._ones,
                "zeros": self._zeros,
                "identity": self._identity,
                "conj": lambda z: z.conjugate() if isinstance(z, complex) else z,
                "re": lambda z: z.real if isinstance(z, complex) else z,
                "im": lambda z: z.imag if isinstance(z, complex) else 0.0,
                "arg": lambda z: (
                    math.atan2(z.imag, z.real) if isinstance(z, complex) else 0.0
                ),
                "random": self._random,
                "randomInt": self._random_int,
                "pickRandom": self._pick_random,
                "unit": Unit,
                "number": self._number,
                "string": str,
                "boolean": bool,
                "print": self._print,
                "elementwise_mul": np.multiply,
                "elementwise_div": np.divide,
                "elementwise_pow": np.power,
                "range": self._range,
                "bellNumbers": _bell_numbers,
                "catalan": _catalan,
                "index": index,
                "Index": Index,
                "subset": self._subset,
                "bignumber": self._bignumber,
                "simplify": self.simplify,
                "derivative": self.derivative,
                "sqrtm": self._sqrtm,
                "pow": self._safe_pow,
                "max": self._max,
                "min": self._min,
            }
        )
