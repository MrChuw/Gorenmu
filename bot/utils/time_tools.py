from __future__ import annotations

import asyncio
import enum
from datetime import UTC, datetime, timedelta
from types import TracebackType
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


class _State(enum.Enum):
    CREATED = "created"
    ENTERED = "active"
    EXPIRING = "expiring"
    EXPIRED = "expired"
    EXITED = "finished"


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
            return scale.key if scale else "minute"

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
        """Asynchronous context manager for cancelling overdue coroutines.

        Use `timeout()` or `timeout_at()` rather than instantiating this class directly.
        """

        def __init__(self, when: float | None, delay: float | None) -> None:
            """Schedule a timeout that will trigger at a given loop time.

            - If `when` is `None`, the timeout will never trigger.
            - If `when < loop.time()`, the timeout will trigger on the next
              iteration of the event loop.
            """
            self._state = _State.CREATED

            self._timeout_handler: asyncio.events.TimerHandle | None = None
            self._task: asyncio.tasks.Task | None = None
            self._when = when
            self.time = delay if when else when
            self._start_time: float | None = None
            self._end_time: float | None = None

        def when(self) -> float | None:
            """Return the current deadline."""
            return self._when

        def reschedule(self, when: float | None) -> None:
            """Reschedule the timeout."""
            if self._state is not _State.ENTERED:
                if self._state is _State.CREATED:
                    raise RuntimeError("Timeout has not been entered")
                raise RuntimeError(
                    f"Cannot change state of {self._state.value} Timeout",
                )

            self._when = when

            if self._timeout_handler is not None:
                self._timeout_handler.cancel()

            if when is None:
                self._timeout_handler = None
            else:
                loop = asyncio.events.get_running_loop()
                if when <= loop.time():
                    self._timeout_handler = loop.call_soon(self._on_timeout)  # NOQA
                else:
                    self._timeout_handler = loop.call_at(when, self._on_timeout)  # NOQA

        def expired(self) -> bool:
            """Is timeout expired during execution?"""
            return self._state in (_State.EXPIRING, _State.EXPIRED)

        def __repr__(self) -> str:
            info = ['']
            if self._state is _State.ENTERED:
                when = round(self._when, 3) if self._when is not None else None
                info.append(f"when={when}")
            info_str = ' '.join(info)
            return f"<Timeout [{self._state.value}]{info_str}>"

        async def __aenter__(self) -> TimeTools.Timeout:
            if self._state is not _State.CREATED:
                raise RuntimeError("Timeout has already been entered")
            task = asyncio.tasks.current_task()
            if task is None:
                raise RuntimeError("Timeout should be used inside a task")
            self._state = _State.ENTERED
            self._task = task
            self._start_time = asyncio.get_running_loop().time()
            self._cancelling = self._task.cancelling()
            self.reschedule(self._when)
            return self

        async def __aexit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None,
        ) -> bool | None:
            assert self._state in (_State.ENTERED, _State.EXPIRING)

            if self._timeout_handler is not None:
                self._timeout_handler.cancel()
                self._timeout_handler = None

            if self._state is _State.EXPIRING:
                self._state = _State.EXPIRED

                if self._task.uncancel() <= self._cancelling and exc_type is not None:
                    # Since there are no new cancel requests, we're
                    # handling this.
                    if issubclass(exc_type, asyncio.exceptions.CancelledError):
                        raise TimeoutError from exc_val
                    elif exc_val is not None:
                        self._insert_timeout_error(exc_val)
                        if isinstance(exc_val, ExceptionGroup):
                            for exc in exc_val.exceptions:
                                self._insert_timeout_error(exc)
            elif self._state is _State.ENTERED:
                self._state = _State.EXITED

            return None

        def _on_timeout(self) -> None:
            assert self._state is _State.ENTERED
            self._task.cancel()
            self._end_time = asyncio.get_running_loop().time()
            self._state = _State.EXPIRING
            self._timeout_handler = None

        @staticmethod
        def _insert_timeout_error(exc_val: BaseException) -> None:
            while exc_val.__context__ is not None:
                if isinstance(exc_val.__context__, asyncio.exceptions.CancelledError):
                    te = TimeoutError()
                    te.__context__ = te.__cause__ = exc_val.__context__
                    exc_val.__context__ = te
                    break
                exc_val = exc_val.__context__

        def cancel(self) -> None:
            """Schedule the cancellation for the next iteration of the event loop."""
            if self._state is not _State.ENTERED:
                return

            loop = asyncio.events.get_running_loop()
            if self._timeout_handler is not None:
                self._timeout_handler.cancel()

            self._timeout_handler = loop.call_soon(self._on_timeout)  # NOQA

        @staticmethod
        def timeout(delay: float | None) -> TimeTools.Timeout:
            loop = asyncio.events.get_running_loop()
            return TimeTools.Timeout(loop.time() + delay if delay is not None else None, delay=delay)

        @staticmethod
        def timeout_at(when: float | None) -> TimeTools.Timeout:
            return TimeTools.Timeout(when, delay=when)

        def cancel_now(self) -> None:
            """Executes the cancellation immediately in the current frame."""
            if self._state is not _State.ENTERED:
                return

            if self._timeout_handler is not None:
                self._timeout_handler.cancel()
                self._timeout_handler = None

            self._on_timeout()

        def duration(self) -> float | None:
            """Returns the actual elapsed time in seconds (float)."""
            if self._start_time is None:
                return None
            end = self._end_time or asyncio.get_running_loop().time()
            return end - self._start_time

        def remaining(self) -> timedelta:
            """Returns the amount of time remaining until the timeout, expressed as timedelta."""
            if self._when is None:
                return timedelta.max

            loop = asyncio.get_running_loop()
            rem = max(0, self._when - loop.time())  # NOQA
            return timedelta(seconds=rem)

        def deadline(self) -> datetime | None:
            """Returns the exact timeout time in UTC datetime."""
            if self._when is None:
                return None

            loop = asyncio.get_running_loop()
            offset = datetime.now(UTC).timestamp() - loop.time()
            return datetime.fromtimestamp(self._when + offset, tz=UTC)
