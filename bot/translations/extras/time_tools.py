# -*- coding: utf-8 -*-

import re
from datetime import datetime, timedelta, timezone
from typing import Optional, Union
from dataclasses import dataclass
import dateutil.parser
from .response import BaseFunctions



@dataclass
class TimeUnitsBase:
    def __init__(self, data: dict):
        assert isinstance(data, dict)
        self.years = data.get("years")
        self.months = data.get("months")
        self.weeks = data.get("weeks")
        self.days = data.get("days")
        self.hours = data.get("hours")
        self.minutes = data.get("minutes")
        self.seconds = data.get("seconds")
        self.milliseconds = data.get("milliseconds")
        self.microseconds = data.get("microseconds")


@dataclass
class TimeUnits:
    def __init__(self, data: dict):
        assert isinstance(data, dict)
        self.singular = TimeUnitsBase(data.get("singular"))
        self.plural = TimeUnitsBase(data.get("plural"))
        self.short = TimeUnitsBase(data.get("short"))


class ParseTime(BaseFunctions):
    def __init__(self, translation: dict, fallback=None) -> None:
        super().__init__(translation, fallback)
        self.strftime = self.get_object('strftime_str')  # NOQA
        self.dayfirst = self._day_first()  # NOQA
        self.yearfirst = self._year_first()  # NOQA
        self.parserinfo = dateutil.parser.parserinfo(dayfirst=self.dayfirst, yearfirst=self.yearfirst)  # NOQA
        self.parser = dateutil.parser.parser(self.parserinfo)


    def __call__(self, target: str) -> Optional[datetime]:
        now = datetime.now(timezone.utc)
        target = target.replace("/", "-")

        if ":" not in target:
            target += f" 12:00:00"

        if "-" in target:
            parts = target.split(" ")
            for i, part in enumerate(parts):
                if "-" in part:
                    if len(part.split("-")) == 2:
                        parts[i] = f"{part}-{now.year}"
                    elif len(part.split("-")) == 1:
                        parts[i] = f"{part}-{now.month}-{now.year}"
            target = " ".join(parts)

        try:
            return self.parser.parse(target)
        except ValueError:
            return None

    def _day_first(self) -> bool:
        splited = self.strftime.split(" ")
        for item in splited:
            if item.startswith("%d"):
                return True
        return False

    def _year_first(self) -> bool:
        splited = self.strftime.split(" ")
        for item in splited:
            if item.startswith("%Y"):
                return True
        return False


class TimeTools(BaseFunctions):
    def __init__(self, translation: dict, fallback=None) -> None:
        super().__init__(translation, fallback)
        self.strftime = self.get_object("strftime_str")
        self.PATTERN_TIME = self.generate_time_regex(self.get_object("Pattern time"))
        self.time_units = TimeUnits(self.get_object("Time Units"))
        self.parse_time = ParseTime(self.obj, self.fallback)


    @staticmethod
    def generate_time_regex(time_units: dict) -> re.Pattern:
        patterns = []
        for unit, terms in time_units.items():
            if unit == "time":
                continue
            patterns.append(rf"(\b(?P<{unit}>\d+)\s?(?:{'|'.join(terms)})\b\s?)?")
        return re.compile(r"\n".join(patterns), re.VERBOSE)

    @staticmethod
    def clean(target: Union[datetime, timedelta]) -> Union[datetime, str]:
        if isinstance(target, timedelta):
            return str(target).split(".")[0]
        if isinstance(target, datetime):
            return target.replace(tzinfo=timezone.utc).replace(microsecond=0)

    def find_relative_time(self, target: str) -> Optional[datetime]:
        match = self.PATTERN_TIME.match(target)
        if match and any(match.groups()[1:]):
            return self.parse_time(target)
        return None

    def find_absolute_time(self, target: str) -> Optional[datetime]:
        match = self.parse_time(target)
        if match:
            return match
        return None

    def format(self, target: datetime) -> str:
        return (target - timedelta(hours=3)).strftime(self.strftime)

    def on_cooldown(self, target: datetime, now: datetime = None, s: int = 0) -> Optional[timedelta]:
        now = now or datetime.now()
        delta = self.clean(now) - self.clean(target)
        if delta.total_seconds() <= s:
            return timedelta(seconds=s) - delta
