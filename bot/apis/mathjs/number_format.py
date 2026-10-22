from __future__ import annotations

from decimal import Decimal, localcontext
from typing import Any

from .format_options import DEFAULT_FORMAT_OPTIONS, FormatOptions, Notation


def _to_decimal(num: Any) -> Decimal:
    if isinstance(num, Decimal):
        return num
    if hasattr(num, 'item'):
        num = num.item()
    if isinstance(num, int):
        return Decimal(num)
    return Decimal(repr(num))


def _exponent_of(d: Decimal) -> int:
    if d == 0:
        return 0
    return d.adjusted()


def _format_exponential(num: Any, precision: int | None) -> str:
    d = _to_decimal(num)
    prec = precision if precision is not None else 6
    with localcontext() as ctx:
        ctx.prec = max(ctx.prec, prec + 10)
        formatted = f"{d:.{prec}E}"
    mantissa, exp = formatted.split('E')
    if precision is None and '.' in mantissa:
        mantissa = mantissa.rstrip('0').rstrip('.')
    exp_int = int(exp)
    return f"{mantissa}e{'+' if exp_int >= 0 else ''}{exp_int}"


def _format_engineering(num: Any, precision: int | None) -> str:
    d = _to_decimal(num)
    if d == 0:
        return "0e+0"
    exp = _exponent_of(d)
    eng_exp = exp - (exp % 3)
    prec = precision if precision is not None else 6
    with localcontext() as ctx:
        ctx.prec = max(ctx.prec, prec + 10)
        mantissa = d / (Decimal(10) ** eng_exp)
        mantissa_str = f"{mantissa:.{prec}f}"
    if precision is None and '.' in mantissa_str:
        mantissa_str = mantissa_str.rstrip('0').rstrip('.')
    return f"{mantissa_str}e{'+' if eng_exp >= 0 else ''}{eng_exp}"


def _format_fixed(num: Any, precision: int | None) -> str:
    if precision is not None:
        d = _to_decimal(num)
        with localcontext() as ctx:
            ctx.prec = max(ctx.prec, d.adjusted() + precision + 10)
            quant = Decimal(1).scaleb(-precision)
            return str(d.quantize(quant))

    if isinstance(num, Decimal):
        return format(num, 'f')
    if isinstance(num, int) and not isinstance(num, bool):
        return str(num)
    if isinstance(num, float):
        if num.is_integer() and abs(num) < 1e16:
            return str(int(num))
        s = f"{num:.15f}".rstrip('0').rstrip('.')
        return s if s else "0"
    return str(num)


def format_number(num: Any, options: FormatOptions | None = None) -> str:
    if isinstance(num, bool):
        return str(num).lower()

    opts = options if options is not None else DEFAULT_FORMAT_OPTIONS

    if num == 0:
        return "0"

    if opts.notation is Notation.FIXED:
        return _format_fixed(num, opts.precision)

    if opts.notation is Notation.EXPONENTIAL:
        return _format_exponential(num, opts.precision)

    if opts.notation is Notation.ENGINEERING:
        return _format_engineering(num, opts.precision)

    exp = _exponent_of(_to_decimal(num))
    if exp < opts.lower_exp or exp >= opts.upper_exp:
        return _format_exponential(num, opts.precision)
    return _format_fixed(num, opts.precision)
