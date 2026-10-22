from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum


class Notation(Enum):
    AUTO = 'auto'
    FIXED = 'fixed'
    EXPONENTIAL = 'exponential'
    ENGINEERING = 'engineering'


@dataclass()
class FormatOptions:
    notation: Notation = Notation.AUTO
    precision: int | None = None
    lower_exp: int = -4
    upper_exp: int = 6
    truncate_matrix: bool = True
    threshold: int = 20
    edge_items: int = 3
    pretty: bool = False
    indent: int = 2

    def with_(self, **changes) -> FormatOptions:
        return replace(self, **changes)

    def __post_init__(self) -> None:
        if not isinstance(self.notation, Notation):
            valid = ', '.join(n.name for n in Notation)
            raise TypeError(
                f"notation must be a Notation (e.g. Notation.FIXED), got {self.notation!r}. Valid values: {valid}",
                "ERR_TYPE",
            )
        if not isinstance(self.indent, int) or self.indent < 0:
            raise ValueError(f"indent must be an integer >= 0, got {self.indent!r}", "ERR_VALUE")


DEFAULT_FORMAT_OPTIONS = FormatOptions()
