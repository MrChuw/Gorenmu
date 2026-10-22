from __future__ import annotations

from decimal import Decimal
from typing import Any

from .format_options import DEFAULT_FORMAT_OPTIONS, FormatOptions
from .matrix import Matrix
from .number_format import format_number
from .unit import Unit


def _format_leaf(value: Any, options: FormatOptions) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, (int, float, Decimal)):
        return format_number(value, options)
    if isinstance(value, complex):
        return _format_complex(value, options)
    if value is None:
        return 'null'
    if isinstance(value, str):
        return f'"{value}"'
    return str(value)


def _format_complex(value: complex, options: FormatOptions) -> str:
    real = value.real
    imag = value.imag

    if imag == 0:
        return format_number(real, options)

    if real == 0:
        if imag == 1:
            return "i"
        if imag == -1:
            return "-i"
        return f"{format_number(imag, options)}i"

    real_str = format_number(real, options)
    imag_abs = abs(imag)
    sign = '+' if imag > 0 else '-'
    if imag_abs == 1:
        imag_str = "i"
    else:
        imag_str = f"{format_number(imag_abs, options)}i"
    return f"{real_str}{sign}{imag_str}"


def _format_nested(data: Any, options: FormatOptions, depth: int = 0) -> str:
    if not isinstance(data, list):
        return _format_leaf(data, options)

    truncate = options.truncate_matrix and len(data) > options.threshold
    has_nested_children = any(isinstance(x, list) for x in data)
    pretty = options.pretty and has_nested_children

    if truncate:
        head, tail = data[:options.edge_items], data[-options.edge_items:]
        head_fmt = [_format_nested(x, options, depth + 1) for x in head]
        tail_fmt = [_format_nested(x, options, depth + 1) for x in tail]
        if pretty:
            items = [*head_fmt, '...', *tail_fmt]
            return _wrap_pretty(items, options, depth)
        return '[' + ', '.join(head_fmt) + ', ... ' + ', '.join(tail_fmt) + ']'

    items = [_format_nested(x, options, depth + 1) for x in data]
    if pretty and items:
        return _wrap_pretty(items, options, depth)
    return '[' + ', '.join(items) + ']'


def _wrap_pretty(items: list[str], options: FormatOptions, depth: int) -> str:
    inner_indent = ' ' * (options.indent * (depth + 1))
    closing_indent = ' ' * (options.indent * depth)
    body = ',\n'.join(f"{inner_indent}{item}" for item in items)
    return f"[\n{body}\n{closing_indent}]"


def format_value(value: Any, options: FormatOptions | None = None) -> str:
    opts = options if options is not None else DEFAULT_FORMAT_OPTIONS

    if isinstance(value, Unit):
        value_str = format_number(value.value, opts)
        return f"{value_str} {value.unit}"

    if isinstance(value, Matrix):
        return _format_nested(value.tolist(), opts)

    if isinstance(value, (list, tuple)):
        return _format_nested(list(value), opts)

    return _format_leaf(value, opts)
