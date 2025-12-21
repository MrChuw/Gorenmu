from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING

from bot.utils.singleton import Singleton

from .timelength import English, Guess, Locale, Portuguese, Spanish, TimeLength
from .timelength.parsers.date_parser import DateParserConfig, preprocess_dates

if TYPE_CHECKING:
    from bot.bot import Context

__all__ = [
    preprocess_dates,
    DateParserConfig,
    English,
    Spanish,
    Guess,
    TimeLength,
    Portuguese,
    "TimeTools",
]

# tl = TimeLength("12:12:12 em 01/01/30", locale=Portuguese())


class TimeTools(metaclass=Singleton):
    def __init__(self):
        self.TimeConvert = self.TimeConvert()

    def teste(self): ...

    class TimeConvert:
        def __init__(self):
            self.tl: TimeLength | None = None

        def convert_text(self, text: str, locale: Locale) -> TimeLength:
            tl = TimeLength(text, locale=locale)
            self.tl: TimeLength = tl
            return tl

        def to_time(self, what: str | None, ctx: Context) -> tuple[datetime, str] | tuple[timedelta, str]:
            mode = None
            if what is None:
                for invalid in self.tl.result.invalid:
                    mode = invalid[0]
                    break
            else:
                mode = what

            dt = self.tl.result.date
            now = datetime.now(ctx.user.tz or UTC)
            base = dt or now

            if dt and dt + self.tl.result.delta >= now.replace(microsecond=0):
                mode = self.tl.locale.now.singular
            elif dt and dt + self.tl.result.delta <= now.replace(microsecond=0):
                mode = self.tl.locale.past.singular

            if mode in self.tl.locale.past.terms:
                return self.tl.ago(base=base), mode
            elif mode in self.tl.locale.now.terms or mode in self.tl.locale.future.terms:
                return self.tl.hence(base=base), mode
            elif mode == 'delta':
                return self.tl.result.delta, mode
            else:
                return self.tl.result.delta, mode

        @staticmethod
        def get_unit(term: str, lang: Locale):
            scale = lang.get_scale(term)
            return scale.singular

        @staticmethod
        def get_units(term: str, lang: Locale):
            scale = lang.get_scale(term)
            return scale.plural

        @staticmethod
        def get_key(term: str, lang: Locale):
            scale = lang.get_scale(term)
            if not scale:
                return "minute"
            return scale.key

        def get_real_unit(self, term: str, lang: Locale):
            key = self.get_key(term=term, lang=lang)
            times = {
                "past": "past",
                "now": "now",
                "future": "future",
                "raw": "time",
                "microsecond": "microseconds",
                "millisecond": "milliseconds",
                "second": "seconds",
                "minute": "minutes",
                "hour": "hours",
                "day": "days",
                "week": "weeks",
                "month": "months",
                "year": "years",
                "decade": "decades",
                "century": "centuries",
                "default": "now",
            }
            return times.get(key, times["default"])

        def to_any(self, asked: str):
            time = 0
            if asked == "delta":
                time = self.tl.to_timedelta()
            elif asked == "microseconds":
                time = self.tl.to_microseconds()
            elif asked == "milliseconds":
                time = self.tl.to_milliseconds()
            elif asked == "seconds":
                time = self.tl.to_seconds()
            elif asked == "minutes":
                time = self.tl.to_minutes()
            elif asked == "hours":
                time = self.tl.to_hours()
            elif asked == "days":
                time = self.tl.to_days()
            elif asked == "weeks":
                time = self.tl.to_weeks()
            elif asked == "months":
                time = self.tl.to_months()
            elif asked == "years":
                time = self.tl.to_years()
            elif asked == "decades":
                time = self.tl.to_decades()
            elif asked == "centuries":
                time = self.tl.to_centuries()
            return time

        @staticmethod
        def to_supress(unit: str):
            if unit in {"raw", "time"}:
                return []
            elif unit == "microseconds":
                return ["years", "months", "days", "hours", "minutes", "seconds", "milliseconds"]
            elif unit == "milliseconds":
                return ["years", "months", "days", "hours", "minutes", "seconds", "microseconds"]
            elif unit == "seconds":
                return ["years", "months", "days", "hours", "minutes", "milliseconds", "microseconds"]
            elif unit == "minutes":
                return ["years", "months", "days", "hours", "seconds", "milliseconds", "microseconds"]
            elif unit == "hours":
                return ["years", "months", "days", "minutes", "seconds", "milliseconds", "microseconds"]
            elif unit in {"days", "weeks"}:
                return ["years", "months", "hours", "minutes", "seconds", "milliseconds", "microseconds"]
            elif unit == "months":
                return ["years", "days", "hours", "minutes", "seconds", "milliseconds", "microseconds"]
            elif unit == "years":
                return ["months", "days", "hours", "minutes", "seconds", "milliseconds", "microseconds"]
            elif unit == "decades":
                return ["years", "days", "hours", "minutes", "seconds", "milliseconds", "microseconds"]
            elif unit == "centuries":
                return ["months", "days", "hours", "minutes", "seconds", "milliseconds", "microseconds"]
            else:
                return []

    TimeConvert: TimeConvert

    class Timeout:
        def __init__(self, timeout: float):
            self.timeout = timeout
            self.start_time = None
            self._task = None
            self._timeout_handle = None
            self.error = asyncio.CancelledError

        def still_valid(self) -> bool:
            if not self.start_time:
                self.start_time = asyncio.get_event_loop().time()
            return not self.expired()

        def expired(self) -> bool:
            return self.elapsed() >= self.timeout

        def elapsed(self) -> float:
            return asyncio.get_event_loop().time() - self.start_time

        def remaining(self) -> float:
            return max(0, self.timeout - self.elapsed())  # NOQA

        def reset(self):
            self.start_time = asyncio.get_event_loop().time()

        async def __aenter__(self):
            self.start_time = asyncio.get_event_loop().time()
            self._task = asyncio.current_task()
            self._timeout_handle = asyncio.get_event_loop().call_later(self.timeout, self._cancel_task)  # NOQA
            return self

        async def __aexit__(self, exc_type, exc, tb):
            if self._timeout_handle:
                self._timeout_handle.cancel()
            return isinstance(exc, asyncio.CancelledError)

        def _cancel_task(self):
            if self._task:
                self._task.cancel()
