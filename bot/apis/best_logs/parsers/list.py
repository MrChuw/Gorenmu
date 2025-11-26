from dataclasses import dataclass
from typing import Any, TypeVar

from .shared import (
    from_list,
    from_none,
    from_str,
    from_union,
    is_type,
    to_class,
)

T = TypeVar("T")


@dataclass
class AvailableLog:
    year: int | None = None
    month: int | None = None

    @staticmethod
    def from_dict(obj: Any) -> "AvailableLog":
        assert isinstance(obj, dict)
        year = from_union([from_none, lambda x: int(from_str(x))], obj.get("year"))
        month = from_union([from_none, lambda x: int(from_str(x))], obj.get("month"))
        return AvailableLog(year, month)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.year is not None:
            result["year"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x)),
                ],
                self.year,
            )
        if self.month is not None:
            result["month"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x)),
                ],
                self.month,
            )
        return result


@dataclass
class List:
    available_logs: list[AvailableLog] | None = None

    @staticmethod
    def from_dict(obj: Any) -> "List":
        assert isinstance(obj, dict)
        available_logs = from_union(
            [lambda x: from_list(AvailableLog.from_dict, x), from_none],
            obj.get("availableLogs"),
        )
        return List(available_logs)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.available_logs is not None:
            result["availableLogs"] = from_union(
                [
                    lambda x: from_list(lambda x: to_class(AvailableLog, x), x),
                    from_none,
                ],
                self.available_logs,
            )
        return result


def purple_list_from_dict(s: Any) -> List:
    return List.from_dict(s)


def purple_list_to_dict(x: List) -> Any:
    return to_class(List, x)
