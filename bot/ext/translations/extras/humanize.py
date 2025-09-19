# -*- coding: utf-8 -*-
from datetime import UTC, datetime
from typing import Dict, List

import humanize


class HumanizeContext:
    def __init__(self, lang):
        self.lang = lang

    def __enter__(self):
        if self.lang != "en":
            humanize.activate(self.lang)

    def __exit__(self, exc_type, exc_val, exc_tb):
        humanize.deactivate()


class Humanize:
    def __init__(self, pattern_time: dict, lang: str, fallback_pattern: dict = None):
        self.lang = lang
        self.units: Dict[str, List[str]]
        pattern = pattern_time
        if fallback_pattern:
            pattern = pattern_time | fallback_pattern
        self._generate_options(pattern)
        self.pattern = pattern

    def precisedelta(self, value, minimum_unit="seconds", suppress=(), format="%0.2f") -> str:
        with HumanizeContext(self.lang):
            response = humanize.precisedelta(value, minimum_unit=minimum_unit, suppress=suppress, format=format)
        return response

    def naturaltime(
        self, value, future: bool = False, months: bool = True, minimum_unit: str = "seconds", when: datetime = None
    ) -> str:
        with HumanizeContext(self.lang):
            response = humanize.naturaltime(value, future=future, months=months, minimum_unit=minimum_unit, when=when)
        return response

    def naturaldelta(self, value, months: bool = True, minimum_unit: str = "seconds") -> str:
        with HumanizeContext(self.lang):
            response = humanize.naturaldelta(value, months=months, minimum_unit=minimum_unit)
        return response

    def naturaldate(self, value) -> str:
        with HumanizeContext(self.lang):
            response = humanize.naturaldate(value)
        return response

    def naturalsize(self, value, binary: bool = False, gnu: bool = False, format: str = "%.1f") -> str:
        with HumanizeContext(self.lang):
            response = humanize.naturalsize(value, binary=binary, gnu=gnu, format=format)
        return response

    def _generate_options(self, units: dict):
        all_units_set = set(units.keys())
        options = {}
        for unit, aliases in units.items():
            if unit == "weeks":  # sourcery skip: merge-duplicate-blocks
                target_units = all_units_set - {"weeks", "days", "months"}
            elif unit in ("days", "months"):
                target_units = all_units_set - {unit, "weeks"}  # NOQA
            else:
                target_units = all_units_set - {unit, "weeks"}

            for alias in aliases:
                options[alias] = [] if unit == "time" else list(target_units)
        self.units = options

    @staticmethod
    def created_a_time(created_at: datetime, timezone=UTC):
        return humanize.precisedelta(datetime.now(timezone) - created_at.astimezone(timezone))

    @staticmethod
    def updated_a_time(updated_at: datetime, timezone=UTC):
        return humanize.precisedelta(datetime.now(timezone) - updated_at.astimezone(timezone))
