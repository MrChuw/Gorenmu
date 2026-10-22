import ast
import contextlib
import math
import operator as op
import random
import re
import signal
from collections.abc import Sequence
from decimal import Decimal
from typing import Any

import numpy as np

from .matrix import Index, Matrix, index
from .unit import Unit

try:
    import resource
except ImportError:
    resource = None


class MathFunction:
    __slots__ = ("_func", "name", "params")

    def __init__(self, func: Any, name: str, params: list[str]) -> None:
        self._func = func
        self.name = name
        self.params = params

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self._func(*args, **kwargs)

    def __repr__(self) -> str:
        return f"{self.name}({', '.join(self.params)})"

    __str__ = __repr__


class MathjsCore:
    def __init__(
        self,
        precision: int = 64,
        max_depth: int = 50,
        max_digits: int = 100_000,
        timeout_seconds: float | None = None,
        max_memory_mb: int | None = None,
    ) -> None:
        self.precision = precision
        self.max_depth = max_depth
        self.max_digits = max_digits
        self.timeout_seconds = timeout_seconds
        self.max_memory_mb = max_memory_mb

        self.scope: dict[str, Any] = {}

        self.scope["_wrap_named_function"] = self._wrap_named_function

        if self.max_memory_mb is not None:
            self._apply_memory_limit(self.max_memory_mb)

        self._bin_ops = {
            ast.Add: op.add,
            ast.Sub: op.sub,
            ast.Mult: op.mul,
            ast.Div: op.truediv,
            ast.FloorDiv: op.floordiv,
            ast.Mod: op.mod,
            ast.Pow: self._safe_pow,
            ast.MatMult: op.matmul,
        }

        self._unary_ops = {
            ast.UAdd: op.pos,
            ast.USub: op.neg,
            ast.Not: op.not_,
            ast.Invert: op.invert,
        }

        self._cmp_ops = {
            ast.Eq: op.eq,
            ast.NotEq: op.ne,
            ast.Lt: op.lt,
            ast.LtE: op.le,
            ast.Gt: op.gt,
            ast.GtE: op.ge,
        }

        self._bool_ops = {
            ast.And: lambda x, y: x and y,
            ast.Or: lambda x, y: x or y,
        }

    @staticmethod
    def _apply_memory_limit(max_memory_mb: int) -> None:
        if resource is None:
            return
        max_bytes = max_memory_mb * 1024 * 1024
        with contextlib.suppress(ValueError, OSError):
            _soft, hard = resource.getrlimit(resource.RLIMIT_AS)
            new_limit = (
                max_bytes if hard == resource.RLIM_INFINITY else min(max_bytes, hard)
            )
            resource.setrlimit(resource.RLIMIT_AS, (new_limit, hard))

    @contextlib.contextmanager
    def _time_limit(self, seconds: float | None):
        if seconds is None or not hasattr(signal, "SIGALRM"):
            yield
            return

        def _handler(signum, frame):
            raise TimeoutError(
                f"Evaluation exceeded the configured time limit ({seconds}s).",
                seconds,
                "ERR_TIMEOUT",
            )

        previous_handler = signal.signal(signal.SIGALRM, _handler)
        signal.setitimer(signal.ITIMER_REAL, seconds)
        try:
            yield
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, previous_handler)

    @staticmethod
    def _log10_magnitude(value: Any) -> float | None:
        if isinstance(value, bool):
            return 0.0
        if isinstance(value, int):
            if value == 0:
                return None
            try:
                return math.log10(abs(value))
            except OverflowError:
                return abs(value).bit_length() * math.log10(2)
        if isinstance(value, float):
            if value == 0 or not math.isfinite(value):
                return None
            return math.log10(abs(value))
        if isinstance(value, Decimal):
            return None if value == 0 else float(value.adjusted())
        return None

    def _safe_pow(self, base: Any, exponent: Any) -> Any:
        if isinstance(base, (int, float, Decimal)) and isinstance(
            exponent, (int, float, Decimal)
        ):  # noqa: SIM102
            if base_log10 := self._log10_magnitude(base):
                try:
                    exp_value = float(exponent)
                    if not math.isfinite(exp_value):
                        exp_value = None
                except OverflowError:
                    exp_value = math.inf

                if exp_value is not None:
                    estimated_result_digits = abs(base_log10) * abs(exp_value) + 1
                    if estimated_result_digits > self.max_digits:
                        raise OverflowError(
                            f"Result of {base!r} ** {exponent!r} would have ~"
                            f"{estimated_result_digits:.0f} digits, which exceeds "
                            f"the configured limit ({self.max_digits}).",
                            self.max_digits,
                            "ERR_OVERFLOW",
                        )
        return op.pow(base, exponent)

    def _safe_factorial(self, n: int) -> int:
        if isinstance(n, int) and n > 1:
            estimated_digits = (
                n * math.log10(n)
                - n * math.log10(math.e)
                + 0.5 * math.log10(2 * math.pi * n)
                + 1
            )
            if estimated_digits > self.max_digits:
                raise OverflowError(
                    f"factorial({n}) would have ~{estimated_digits:.0f} digits, "
                    f"which exceeds the configured limit ({self.max_digits}).",
                    self.max_digits,
                    "ERR_OVERFLOW",
                )
        return math.factorial(n)

    def _eval_ast(
        self, node: ast.AST, local_scope: dict[str, Any], depth: int = 0
    ) -> Any:
        if depth > self.max_depth:
            raise RecursionError(
                f"Expression too complex: depth limit ({self.max_depth}) exceeded.",
                self.max_depth,
                "ERR_RECURSION",
            )

        if isinstance(node, ast.Constant):
            return node.value

        if isinstance(node, ast.Name):
            if node.id in local_scope:
                return local_scope[node.id]
            if node.id in self.scope:
                return self.scope[node.id]
            raise NameError(f"name '{node.id}' is not defined", node.id, "ERR_NAME")

        if isinstance(node, ast.List):
            return [self._eval_ast(elt, local_scope, depth + 1) for elt in node.elts]
        if isinstance(node, ast.Tuple):
            return tuple(
                self._eval_ast(elt, local_scope, depth + 1) for elt in node.elts
            )

        if isinstance(node, ast.BinOp):
            left = self._eval_ast(node.left, local_scope, depth + 1)
            right = self._eval_ast(node.right, local_scope, depth + 1)
            op_func = self._bin_ops.get(type(node.op))  # noqa
            if op_func is None:
                raise NotImplementedError(
                    f"Binary operator {type(node.op)} not supported",
                    node.op,
                    "ERR_NOT_IMPLEMENTED",
                )
            return op_func(left, right)

        if isinstance(node, ast.UnaryOp):
            operand = self._eval_ast(node.operand, local_scope, depth + 1)
            op_func = self._unary_ops.get(type(node.op))  # noqa
            if op_func is None:
                raise NotImplementedError(
                    f"Unary operator {type(node.op)} not supported",
                    node.op,
                    "ERR_NOT_IMPLEMENTED",
                )
            return op_func(operand)

        if isinstance(node, ast.BoolOp):
            op_func = self._bool_ops[type(node.op)]  # noqa
            values = [self._eval_ast(v, local_scope, depth + 1) for v in node.values]
            result = values[0]
            for v in values[1:]:
                result = op_func(result, v)
            return result

        if isinstance(node, ast.Compare):
            left = self._eval_ast(node.left, local_scope, depth + 1)
            for cmp_op, cmp_node in zip(node.ops, node.comparators, strict=False):
                right = self._eval_ast(cmp_node, local_scope, depth + 1)
                cmp_func = self._cmp_ops.get(type(cmp_op))  # noqa
                if cmp_func is None:
                    raise NotImplementedError(
                        f"Comparison {type(cmp_op)} not supported",
                        cmp_op,
                        "ERR_NOT_IMPLEMENTED",
                    )
                if not cmp_func(left, right):
                    return False
                left = right
            return True

        if isinstance(node, ast.IfExp):
            cond = self._eval_ast(node.test, local_scope, depth + 1)
            if cond:
                return self._eval_ast(node.body, local_scope, depth + 1)
            return self._eval_ast(node.orelse, local_scope, depth + 1)

        if isinstance(node, ast.Call):
            func = self._eval_ast(node.func, local_scope, depth + 1)
            args = [self._eval_ast(arg, local_scope, depth + 1) for arg in node.args]
            kwargs = {
                kw.arg: self._eval_ast(kw.value, local_scope, depth + 1)
                for kw in node.keywords
            }
            return func(*args, **kwargs)

        if isinstance(node, ast.Attribute):
            obj = self._eval_ast(node.value, local_scope, depth + 1)
            return getattr(obj, node.attr)

        if isinstance(node, ast.Subscript):
            obj = self._eval_ast(node.value, local_scope, depth + 1)
            idx = self._eval_ast(node.slice, local_scope, depth + 1)
            return obj[idx]

        if isinstance(node, ast.Lambda):
            lambda_node = node

            def lambda_func(
                *args, _node=lambda_node, _self=self, _local=local_scope, _depth=depth
            ):  # noqa
                call_scope = _local.copy()
                for param, arg in zip(_node.args.args, args, strict=False):
                    call_scope[param.arg] = arg
                return _self._eval_ast(_node.body, call_scope, _depth + 1)

            return lambda_func

        raise NotImplementedError(
            f"AST node {type(node).__name__} not supported",
            type(node).__name__,
            "ERR_NOT_IMPLEMENTED",
        )

    def _exec_stmt(self, stmt: str, local_scope: dict[str, Any]) -> Any:
        try:
            tree = ast.parse(stmt, mode="eval")
            return self._eval_ast(tree.body, local_scope)
        except SyntaxError as e:
            tree = ast.parse(stmt, mode="exec")
            value = None
            for node in tree.body:
                if isinstance(node, ast.Expr):
                    value = self._eval_ast(node.value, local_scope)
                elif isinstance(node, ast.Assign):
                    value = self._eval_ast(node.value, local_scope)
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            local_scope[target.id] = value
                        else:
                            raise NotImplementedError(  # noqa: B904
                                "Only simple variable assignments are supported",
                                "ERR_NOT_IMPLEMENTED",
                            )
                else:
                    raise NotImplementedError(  # noqa: B904
                        f"Statement type {type(node).__name__} not supported",
                        type(node).__name__,
                        "ERR_NOT_IMPLEMENTED",
                    )
            return value

    @staticmethod
    def _to_array(args: tuple[Any, ...]) -> Sequence[float] | tuple[Any, ...]:
        """Unwraps a single sequence argument or returns args as a tuple."""
        if len(args) == 1 and isinstance(args[0], Sequence):
            return args[0]
        return args

    def _max(self, *args: float | Sequence[float]) -> float:
        data = self._to_array(args)
        return float(np.max(data))

    def _min(self, *args: float | Sequence[float]) -> float:
        data = self._to_array(args)
        return float(np.min(data))

    def _sum(self, *args: float | Sequence[float]) -> float:
        data = self._to_array(args)
        return float(np.sum(data))

    def _mean(self, *args: float | Sequence[float]) -> float:
        data = self._to_array(args)
        return float(np.mean(data))

    def _median(self, *args: float | Sequence[float]) -> float:
        data = self._to_array(args)
        return float(np.median(data))

    def _std(
        self, *args: float | Sequence[float], normalization: str = "unbiased"
    ) -> float:
        data = self._to_array(args)
        ddof = 0 if normalization == "uncorrected" else 1
        return float(np.std(data, ddof=ddof))

    def _variance(
        self, *args: float | Sequence[float], normalization: str = "unbiased"
    ) -> float:
        data = self._to_array(args)
        ddof = 0 if normalization == "uncorrected" else 1
        return float(np.var(data, ddof=ddof))

    def _prod(self, *args: float | Sequence[float]) -> float:
        data = self._to_array(args)
        return float(np.prod(data))

    @staticmethod
    def _det(a) -> float:
        return float(np.linalg.det(np.asarray(a)))

    @staticmethod
    def _inv(a) -> Matrix:
        return Matrix(np.linalg.inv(np.asarray(a)))

    @staticmethod
    def _transpose(a) -> Matrix:
        return Matrix(np.asarray(a).T)

    @staticmethod
    def _size(a) -> list[int]:
        if isinstance(a, Matrix):
            return list(a.shape)
        if isinstance(a, (list, tuple)):
            return list(np.array(a).shape)
        return [len(a)] if isinstance(a, str) else []

    @staticmethod
    def _norm(a, p: int | float | str = 2) -> int | float:
        a_arr = np.asarray(a)
        if a_arr.ndim == 1:
            if p == "fro":
                p = 2
            return np.linalg.norm(a_arr, ord=p)  # noqa  # ty: ignore[invalid-argument-type]
        if p in ["fro", 2]:
            return np.linalg.norm(a_arr, "fro")  # noqa  # ty: ignore[invalid-argument-type]
        if p == 1:
            return np.linalg.norm(a_arr, 1)  # noqa  # ty: ignore[invalid-argument-type]
        if p in [np.inf, "inf"]:
            return np.linalg.norm(a_arr, np.inf)  # noqa  # ty: ignore[invalid-argument-type]
        return np.linalg.norm(a_arr, p)  # noqa  # ty: ignore[invalid-argument-type]

    @staticmethod
    def _dot(a, b) -> int | float:
        a = np.asarray(a).flatten()
        b = np.asarray(b).flatten()
        return float(np.dot(a, b))

    @staticmethod
    def _cross(a, b) -> Matrix:
        a = np.asarray(a).flatten()
        b = np.asarray(b).flatten()
        if len(a) != 3 or len(b) != 3:
            raise ValueError("Cross product requires 3D vectors", "ERR_MATRIX")
        return Matrix(np.cross(a, b))

    @staticmethod
    def _kron(a, b) -> Matrix:
        return Matrix(np.kron(a, b))

    @staticmethod
    def _ones(*args) -> Matrix:
        if not args:
            return Matrix([[]])
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            return Matrix(np.ones(args[0]))
        return Matrix(np.ones(args))

    @staticmethod
    def _zeros(*args) -> Matrix:
        if not args:
            return Matrix([[]])
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            return Matrix(np.zeros(args[0]))
        return Matrix(np.zeros(args))

    @staticmethod
    def _identity(n: int) -> Matrix:
        return Matrix(np.eye(n))

    @staticmethod
    def _random(*args) -> Any:
        if not args:
            return random.random()
        if len(args) == 1:
            if isinstance(args[0], (list, tuple, Matrix)):
                size = args[0].tolist() if isinstance(args[0], Matrix) else args[0]
                return Matrix(np.random.random(size))
            return random.random() * args[0]
        if len(args) == 2:
            return random.random() * (args[1] - args[0]) + args[0]
        raise ValueError("Invalid arguments to random", "ERR_VALUE")

    @staticmethod
    def _random_int(*args: Any) -> Any:
        if not args:
            return random.randint(0, 1)

        if len(args) == 1:
            if isinstance(args[0], (list, tuple, Matrix)):
                size = args[0].tolist() if isinstance(args[0], Matrix) else args[0]
                return Matrix(np.random.randint(0, 2, size=size))
            return random.randint(0, args[0])

        if len(args) == 2:
            if isinstance(args[0], (list, tuple, Matrix)):
                size = args[0].tolist() if isinstance(args[0], Matrix) else args[0]
                return Matrix(np.random.randint(0, args[1], size=size))
            return random.randint(args[0], args[1])

        if len(args) == 3 and isinstance(args[0], (list, tuple, Matrix)):
            size = args[0].tolist() if isinstance(args[0], Matrix) else args[0]
            return Matrix(np.random.randint(args[1], args[2], size=size))

        raise ValueError("Invalid arguments to randomInt", "ERR_VALUE")

    @staticmethod
    def _pick_random(arr, *args) -> Any:  # noqa
        if isinstance(arr, Matrix):
            arr = arr.tolist()
        return random.choice(arr)

    @staticmethod
    def _number(value: Any) -> int | float:
        if isinstance(value, Decimal):
            return float(value)
        return value.value if isinstance(value, Unit) else float(value)  # noqa

    @staticmethod
    def _subset(matrix, idx, replacement=None):
        if matrix is Matrix:
            matrix = Matrix()
        elif isinstance(matrix, (list, tuple)):
            matrix = Matrix(matrix)
        elif not isinstance(matrix, Matrix):
            matrix = Matrix(matrix if matrix is not None else [])
        return matrix.subset(idx, replacement)

    @staticmethod
    def _range(
        start: int | float,
        end: int | float | None = None,
        step: int | float = 1,
    ) -> Matrix:
        if end is None:
            start, end = 0, start
        if step == 0:
            raise ValueError("step must not be zero", "ERR_VALUE")

        result: list[int | float] = []
        current = (
            float(start)
            if isinstance(start, float)
            or isinstance(step, float)
            or isinstance(end, float)
            else start
        )
        epsilon = 1e-12 if isinstance(current, float) else 0
        if step > 0:
            while current <= end + epsilon:
                result.append(current)
                current += step
        else:
            while current >= end - epsilon:
                result.append(current)
                current += step
        return Matrix(result)

    @staticmethod
    def _print(template: str, values: dict[str, Any] | None = None) -> None:
        if values is None:
            print(template)
            return
        for key, val in values.items():
            template = template.replace(f"${key}", str(val))
        print(template)

    def _transform(self, expr: str) -> str:
        strings: dict[int, str] = {}

        def repl_string(match):
            idx = len(strings)
            strings[idx] = match.group(0)
            return f"__STR_{idx}__"

        expr = re.sub(r'"[^"\\]*(?:\\.[^"\\]*)*"', repl_string, expr)
        expr = re.sub(r"'[^'\\]*(?:\\.[^'\\]*)*'", repl_string, expr)

        expr = self._replace_function_definitions(expr)
        expr = self._replace_elementwise_pow(expr)
        expr = expr.replace("^", "**")
        expr = self._replace_matrices(expr)

        expr = re.sub(r"\bi\b", "1j", expr)
        expr = re.sub(r"(\d+)i", r"\1j", expr)

        expr = re.sub(r"\.\*", "*", expr)
        expr = re.sub(r"\./", "/", expr)

        expr = self._replace_ternary(expr)

        expr = re.sub(
            r"(\d+(?:\.\d+)?)\s*([a-zA-Z]+)\s+to\s+([a-zA-Z]+)",
            r"unit(\1,'\2').to('\3')",
            expr,
        )

        expr = expr.replace("sqrt(-1)", "1j")

        for idx, s in strings.items():
            expr = expr.replace(f"__STR_{idx}__", s)

        return expr

    def _replace_elementwise_pow(self, expr: str) -> str:
        while ".^" in expr:
            pos = expr.index(".^")
            left, left_start = self._extract_left_operand(expr, pos)
            right, right_end = self._extract_right_operand(expr, pos + len(".^"))
            if not left or not right:
                break
            expr = (
                f"{expr[:left_start]}elementwise_pow({left}, {right}){expr[right_end:]}"
            )
        return expr

    @staticmethod
    def _extract_left_operand(expr: str, end: int) -> tuple[str, int]:
        i = end - 1
        while i >= 0 and expr[i] == " ":
            i -= 1
        if i < 0:
            return "", end

        token_end = i + 1
        if expr[i] in ")]":
            closer = expr[i]
            opener = "(" if closer == ")" else "["
            depth = 0
            while i >= 0:
                if expr[i] == closer:
                    depth += 1
                elif expr[i] == opener:
                    depth -= 1
                    if depth == 0:
                        break
                i -= 1
            start = i
            j = start - 1
            while j >= 0 and (expr[j].isalnum() or expr[j] == "_"):
                j -= 1
            start = j + 1
            return expr[start:token_end], start

        j = i
        while j >= 0 and (expr[j].isalnum() or expr[j] in "_."):
            j -= 1
        start = j + 1
        return expr[start:token_end], start

    @staticmethod
    def _extract_right_operand(expr: str, start: int) -> tuple[str, int]:
        i = start
        while i < len(expr) and expr[i] == " ":
            i += 1
        sign_start = i
        if i < len(expr) and expr[i] in "+-":
            i += 1
            while i < len(expr) and expr[i] == " ":
                i += 1
        if i >= len(expr):
            return "", start

        if expr[i] in "([":
            opener = expr[i]
            closer = ")" if opener == "(" else "]"
            depth = 0
            j = i
            while j < len(expr):
                if expr[j] == opener:
                    depth += 1
                elif expr[j] == closer:
                    depth -= 1
                    if depth == 0:
                        j += 1
                        break
                j += 1
            return expr[sign_start:j], j

        j = i
        while j < len(expr) and (expr[j].isalnum() or expr[j] in "_."):
            j += 1
        return expr[sign_start:j], j

    _POLY_TERM_RE_CACHE: dict[str, re.Pattern] = {}

    def _polynomial_term_re(self, var: str) -> re.Pattern:
        pattern = self._POLY_TERM_RE_CACHE.get(var)
        if pattern is None:
            pattern = re.compile(
                rf"^(?P<coef>\d+(?:\.\d+)?)?\*?(?P<var>{re.escape(var)})?(?:\*\*|\^)?(?P<pow>\d+)?$"
            )
            self._POLY_TERM_RE_CACHE[var] = pattern
        return pattern

    def _parse_polynomial(self, expr: str, var: str) -> dict[int, float]:
        e = expr.replace(" ", "")
        if not e:
            raise ValueError("Empty expression", expr, "ERR_POLY")

        e = re.sub(r"(?<!^)(?<![+\-])-", "+-", e)
        terms = [t for t in e.split("+") if t]

        term_re = self._polynomial_term_re(var)
        coeffs: dict[int, float] = {}
        for term in terms:
            sign = 1.0
            t = term
            if t.startswith("-"):
                sign = -1.0
                t = t[1:]
            match = term_re.match(t)
            if not match:
                raise ValueError(
                    f"Could not parse '{term}' as a simple polynomial term in '{var}'",
                    term,
                    "ERR_POLY",
                )
            has_var = match.group("var") is not None
            coef_str = match.group("coef")
            coef = float(coef_str) if coef_str is not None else 1.0
            power = (
                int(match.group("pow")) if match.group("pow") else (1 if has_var else 0)
            )
            coeffs[power] = coeffs.get(power, 0.0) + sign * coef
        return coeffs

    @staticmethod
    def _format_polynomial(coeffs: dict[int, float], var: str) -> str:
        powers = sorted((p for p, c in coeffs.items() if c != 0), reverse=True)
        if not powers:
            return "0"

        def _term(power: int, coef: float) -> str:
            c = int(coef) if float(coef).is_integer() else coef
            if power == 0:
                return f"{abs(c)}"
            base = var if power == 1 else f"{var}^{power}"
            if abs(c) == 1:
                return base
            return f"{abs(c)} * {base}"

        first_power = powers[0]
        first_coef = coeffs[first_power]
        result = ("-" if first_coef < 0 else "") + _term(first_power, first_coef)
        for power in powers[1:]:
            coef = coeffs[power]
            result += (
                f" - {_term(power, coef)}" if coef < 0 else f" + {_term(power, coef)}"
            )
        return result

    def simplify(self, expr: str, var: str = "x") -> str:
        return self._format_polynomial(self._parse_polynomial(expr, var), var)

    def derivative(self, expr: str, var: str = "x") -> str:
        coeffs = self._parse_polynomial(expr, var)
        deriv = {
            power - 1: coef * power for power, coef in coeffs.items() if power >= 1
        }
        return self._format_polynomial(deriv, var)

    @staticmethod
    def _sqrtm(a: Any, iterations: int = 100, tol: float = 1e-12) -> Matrix:
        arr = np.asarray(a, dtype=float)
        if arr.ndim != 2 or arr.shape[0] != arr.shape[1]:
            raise ValueError("sqrtm requires a square matrix", arr.shape, "ERR_MATRIX")

        n = arr.shape[0]
        y = arr.copy()
        z = np.eye(n)
        for _ in range(iterations):
            y_next = 0.5 * (y + np.linalg.inv(z))
            z_next = 0.5 * (z + np.linalg.inv(y))
            if np.allclose(y_next, y, atol=tol):
                y = y_next
                break
            y, z = y_next, z_next
        return Matrix(y)

    def _replace_matrices(self, expr: str) -> str:
        result: list[str] = []
        stack: list[int] = []

        for i, ch in enumerate(expr):
            if ch == "[":
                stack.append(i)
            elif ch == "]" and stack:
                start = stack.pop()
                if not stack:
                    inner = expr[start + 1 : i]
                    inner_processed = self._replace_matrices(inner)

                    if ";" in inner_processed:
                        rows = [row.strip() for row in inner_processed.split(";")]
                        rows_py = [f"[{row}]" for row in rows]
                        matrix_str = f"Matrix([{', '.join(rows_py)}])"
                    else:
                        matrix_str = f"Matrix([{inner_processed}])"

                    result.append(matrix_str)
            elif not stack:
                result.append(ch)

        return "".join(result)

    @staticmethod
    def _replace_ternary(expr: str) -> str:
        def _parse_ternary(s: str) -> str:
            depth = 0
            for i, ch in enumerate(s):
                if ch in "([":
                    depth += 1
                elif ch in ")]":
                    depth -= 1
                elif ch == "?" and depth == 0:
                    depth2 = 0
                    for j in range(i + 1, len(s)):
                        if s[j] in "([":
                            depth2 += 1
                        elif s[j] in ")]":
                            depth2 -= 1
                        elif s[j] == ":" and depth2 == 0:
                            cond = s[:i].strip()
                            true_expr = s[i + 1 : j].strip()
                            false_expr = s[j + 1 :].strip()
                            return f"({true_expr} if {cond} else {false_expr})"
            return s

        changed = True
        while changed:
            new_expr = _parse_ternary(expr)
            changed = new_expr != expr
            expr = new_expr
        return expr

    @staticmethod
    def _split_statements(expr: str) -> list[str]:
        parts: list[str] = []
        current: list[str] = []
        in_string = False
        string_char: str | None = None
        depth = 0
        for ch in expr:
            if ch in ['"', "'"] and not in_string:
                in_string = True
                string_char = ch
                current.append(ch)
                continue
            if ch == string_char and in_string:
                in_string = False
                string_char = None
                current.append(ch)
                continue
            if in_string:
                current.append(ch)
                continue
            if ch in "([{":
                depth += 1
            elif ch in ")]}":
                depth -= 1
            if depth == 0 and ch in [";", "\n"]:
                parts.append("".join(current))
                current = []
            else:
                current.append(ch)
        if current:
            parts.append("".join(current))
        return [p.strip() for p in parts if p.strip()]

    @staticmethod
    def _wrap_named_function(func: Any, name: str, params: list[str]) -> MathFunction:
        return MathFunction(func, name, params)

    @staticmethod
    def _replace_function_definitions(stmt: str) -> str:
        if match := re.match(r"^([a-zA-Z_]\w*)\s*\(([^)]*)\)\s*=\s*(.+)$", stmt):
            name = match.group(1)
            params = [p.strip() for p in match.group(2).split(",") if p.strip()]
            body = match.group(3)
            params_str = ", ".join(params)
            return f"{name} = _wrap_named_function(lambda {params_str}: ({body}), '{name}', {params!r})"
        return stmt


def _bell_numbers(n: int) -> int:
    if n < 0:
        raise ValueError("n must be >= 0", "ERR_VALUE")
    bell = [0] * (n + 1)
    bell[0] = 1
    for i in range(1, n + 1):
        for j in range(i):
            bell[i] += bell[j] * math.comb(i - 1, j)
    return bell[n]


def _catalan(n: int) -> int:
    if n < 0:
        raise ValueError("n must be >= 0", "ERR_VALUE")
    return math.comb(2 * n, n) // (n + 1)
