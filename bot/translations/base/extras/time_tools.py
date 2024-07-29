# -*- coding: utf-8 -*-

import re
from datetime import datetime, timedelta, timezone
from typing import Optional, Union

import humanize


class TimeTools:
    def __init__(self):
        pass

    YEAR: str
    DAY: str
    HOUR: str
    MINUTE: str
    SECOND: str
    YY: str
    DD: str
    HH: str
    MM: str
    SS: str

    PATTERN_TIME: re.Pattern

    pattern_relative_time: re.Pattern

    pattern_absolute_time_and_date: re.Pattern

    def birthday(self, target: str) -> Optional[str]:
        pass

    @staticmethod
    def clean(target: Union[datetime, timedelta]) -> Union[datetime, str]:
        pass

    @staticmethod
    def date_in_full(delta: timedelta) -> str:
        pass

    def find_relative_time(self, target: str) -> Optional[re.Match]:
        pass

    def find_absolute_time(self, target: str) -> Optional[re.Match]:
        pass

    def format(self, target: datetime) -> str:
        pass

    def on_cooldown(self, target: datetime, now: datetime = None, s: int = 0) -> Optional[timedelta]:
        pass

    def timeago(self, target: datetime, now: datetime = None, full: bool = True) -> Union[str, timedelta]:
        pass


class Humanize:
    @staticmethod
    def precisedelta(value, minimum_unit="seconds", suppress=(), format="%0.2f") -> str:
        pass

    @staticmethod
    def naturaltime(value, future: bool = False, months: bool = True, minimum_unit: str = "seconds",
                    when: datetime = None, ) -> str:
        pass

    @staticmethod
    def naturaldelta(value, months: bool = True, minimum_unit: str = "seconds") -> str:
        pass

    @staticmethod
    def naturaldate(value) -> str:
        pass

    @staticmethod
    def naturalsize(value, binary: bool = False, gnu: bool = False, format: str = "%.1f") -> str:
        pass


class Timeago:
    def __init__(self, target: datetime, *, now: datetime = None, reverse: bool = False) -> None:
        if now is None:
            now = datetime.utcnow()
        target = target.replace(tzinfo=None)
        now = now.replace(tzinfo=None)
        if reverse:
            target, now = now, target
        if target > now:
            raise ValueError()
        self.delta = now - target
        yy, dd = divmod(self.delta.days, 365)
        mm, ss = divmod(self.delta.seconds, 60)
        hh, mm = divmod(mm, 60)
        self.years = yy
        self.days = dd
        self.hours = hh
        self.minutes = mm
        self.seconds = ss

    def total_in_seconds(self) -> float:
        pass

    def humanize(self, *, precision: int = 2, minimum: str = "s", short: bool = False) -> str:
        pass
