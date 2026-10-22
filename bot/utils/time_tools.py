from __future__ import annotations

import asyncio
import enum
import re
from collections.abc import Callable
from datetime import UTC, datetime, timedelta, tzinfo
from types import TracebackType
from typing import TYPE_CHECKING, Literal

from bot.utils.singleton import Singleton

from .timelength import English, Guess, Locale, Portuguese, Spanish, TimeLength
from .timelength.dataclasses import Scale
from .timelength.parsers.date_parser import DateParserConfig, preprocess_dates

if TYPE_CHECKING:
    from bot.bot import Context

__all__ = [
    "preprocess_dates",
    "DateParserConfig",
    "English",
    "Spanish",
    "Guess",
    "TimeLength",
    "Portuguese",
    "TimeTools",
]

TimeUnit = Literal[
    "delta",
    "microseconds",
    "milliseconds",
    "seconds",
    "minutes",
    "hours",
    "days",
    "weeks",
    "months",
    "years",
    "decades",
    "centuries",
]

# Every unit, in the order `_convert_dispatch`/`_suppress_dispatch` below reason about them.
_ALL_UNITS: tuple[str, ...] = (
    "years",
    "months",
    "days",
    "hours",
    "minutes",
    "seconds",
    "milliseconds",
    "microseconds",
)


class _State(enum.Enum):
    CREATED = "created"
    ENTERED = "active"
    EXPIRING = "expiring"
    EXPIRED = "expired"
    EXITED = "finished"


class TimeTools(metaclass=Singleton):
    def __init__(self, default_timezone: tzinfo = UTC) -> None:
        self.default_timezone: tzinfo = default_timezone
        self.TimeConvert = self._TimeConvert(default_timezone)

    class _TimeConvert:
        """
        A thin, per-parse manager around `TimeLength`.

        `TimeTools` itself only owns configuration (the default timezone) and the `Timeout`
        helper below; all of the actual duration/date parsing is delegated to `timelength`.
        """

        def __init__(self, default_timezone: tzinfo = UTC) -> None:
            self.default_timezone: tzinfo = default_timezone
            self.tl: TimeLength | None = None

        def convert_text(self, text: str, locale: Locale | Guess, timezone: tzinfo | None = None) -> TimeLength:
            """---
            Parse `text` using `locale`.

            #### Arguments
            - text: `str` — The text to parse. Only pass the portion that actually represents a
                length of time or a date/time — see `TimeTools.split_time_text()` to separate that
                portion out of a larger free-form message first.
            - locale: `Locale | Guess` — The locale context to parse with.
            - timezone: `tzinfo | None = None` — Overrides `self.default_timezone` for this parse only.
                Useful for a user with their own configured timezone, without having to touch
                `self.default_timezone` for everyone else.

            #### Returns
            - The resulting `TimeLength`, also stored on `self.tl` for the other methods below.
            """

            tl = TimeLength(text, locale=locale, timezone=timezone or self.default_timezone)
            self.tl = tl
            return tl

        @staticmethod
        def split_time_text(text: str, locale: Locale | Guess, timezone: tzinfo | None = None) -> tuple[str, str]:
            """---
            Convenience helper for commands like `+remindme <when> about <what>`.

            Parses all of `text` as a `TimeLength` and returns `result.remaining_text`
            (whatever wasn't consumed by the found date/duration) split off from it.

            #### Arguments
            - text: `str` — The full text to parse, e.g. everything after stripping the command name.
            - locale: `Locale | Guess` — The locale context to parse with.
            - timezone: `tzinfo | None = None` — Overrides the timezone used to interpret any date found.

            #### Returns
            - A tuple of `(remaining_text, matched_text)`.
                - `remaining_text` is `text` with the recognized date/duration span(s) removed
                    (see `ParsedTimeLength.remaining_text` for exactly what counts as recognized).
                - `matched_text` is the exact complement: just the recognized span(s), concatenated
                    in their original order. Mainly useful for logging/debugging.

            #### Example
            ```python
            remaining, matched = TimeTools().TimeConvert.split_time_text(
                "as 19:22:22 do dia 12/02/2029 sobre o blablabla", Portuguese()
            )
            # remaining == "as do dia sobre o blablabla"  (the found date's own span is removed;
            #                                               "as"/"do"/"dia" are leftover filler
            #                                               words the parser didn't recognize)
            # matched   == "19:22:2212/02/2029"
            ```
            """

            tl = TimeLength(text, locale=locale, timezone=timezone)
            return tl.result.remaining_text, tl.result.matched_text

        @staticmethod
        def _time_of_day(text: str, now: datetime) -> datetime | None:
            """Interpreta 'HH:MM' ou 'HH:MM:SS' como hoje (ou amanhã, se já passou)."""
            match = re.fullmatch(r"\s*(\d{1,2}):(\d{2})(?::(\d{2}))?\s*", text or "")
            if not match:
                return None

            hour = int(match.group(1))
            minute = int(match.group(2))
            second = int(match.group(3)) if match.group(3) is not None else 0

            if not (0 <= hour < 24 and 0 <= minute < 60 and 0 <= second < 60):
                return None

            target = now.replace(hour=hour, minute=minute, second=second, microsecond=0)
            if target <= now:
                target += timedelta(days=1)
            return target

        def to_time(
            self, what: str | None, timezone: tzinfo | None = None
        ) -> tuple[datetime | timedelta | None, str | float | None]:
            if self.tl is None:
                raise RuntimeError("convert_text() must be called before to_time().")

            result = self.tl.result
            locale = self.tl.locale
            effective_timezone = timezone or self.tl.timezone

            mode = what
            if mode is None and result.invalid:
                mode = result.invalid[0][0]

            dt = result.date.astimezone(effective_timezone) if result.date else None
            now = datetime.now(effective_timezone)
            base = dt or now

            # 1) 'HH:MM' / 'HH:MM:SS' puros → hoje nesse horário, ou amanhã se já passou.
            if dt is None and result.delta is not None:
                tod = self._time_of_day(self.tl.content, now)
                if tod is not None:
                    if mode in locale.past.terms:
                        return self.tl.ago(base=now), mode
                    return tod, mode

            # 2) Se uma data foi encontrada, resolve como instante absoluto: data + delta.
            if dt is not None:
                target = dt + (result.delta or timedelta(0))
                if mode in locale.past.terms:
                    return self.tl.ago(base=dt), mode
                return target, mode

            # 3) Sem data: comportamento baseado em delta.
            if mode in locale.past.terms:
                return self.tl.ago(base=base), mode
            if mode in locale.now.terms or mode in locale.future.terms:
                return self.tl.hence(base=base), mode

            return result.delta, mode

        def _first_invalid_or(self, what: str | None) -> str | float | None:
            if what is not None:
                return what
            if self.tl is None:
                return None
            for invalid_value, _flag in self.tl.result.invalid:
                return invalid_value
            return None

        def to_delta(self, what: str | None) -> tuple[timedelta | None, str | float | None]:
            if self.tl is None:
                raise RuntimeError("convert_text() must be called before to_delta().")
            return self.tl.result.delta, self._first_invalid_or(what)

        def to_hence(
            self, what: str | None, base: datetime | timedelta | None, timezone: tzinfo | None = None
        ) -> tuple[datetime, str | float | None]:
            if self.tl is None:
                raise RuntimeError("convert_text() must be called before to_hence().")

            mode = self._first_invalid_or(what)
            effective_timezone = timezone or self.tl.timezone
            dt = self.tl.result.date
            now = datetime.now(effective_timezone)

            if isinstance(base, datetime):
                resolved_base = base.astimezone(effective_timezone)
            elif isinstance(base, timedelta):
                resolved_base = base + now
            else:
                resolved_base = dt or now

            return self.tl.hence(base=resolved_base), mode

        @staticmethod
        def get_unit(term: str, lang: Locale) -> str:
            scale = lang.get_scale(term)
            return scale.singular if scale else term

        @staticmethod
        def get_units(term: str, lang: Locale) -> str:
            scale = lang.get_scale(term)
            return scale.plural if scale else term

        @staticmethod
        def get_key(term: str, lang: Locale) -> str:
            scale = lang.get_scale(term)
            return scale.key if scale else "minute"

        _REAL_UNIT_BY_KEY: dict[str, str] = {
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
        }

        def get_real_unit(self, term: str, lang: Locale | Guess) -> str:
            key = self.get_key(term=term, lang=lang)  # ty: ignore[invalid-argument-type] # noqa
            return self._REAL_UNIT_BY_KEY.get(key, "now")

        def _convert_dispatch(self) -> dict[str, Callable[[], float | timedelta | None]]:
            """Build the `asked -> callable` table used by `to_any()`, bound to the current `self.tl`."""
            if self.tl is None:
                raise RuntimeError("convert_text() must be called before to_any().")

            tl = self.tl
            return {
                "delta": tl.to_timedelta,
                "microseconds": tl.to_microseconds,
                "milliseconds": tl.to_milliseconds,
                "seconds": tl.to_seconds,
                "minutes": tl.to_minutes,
                "hours": tl.to_hours,
                "days": tl.to_days,
                "weeks": tl.to_weeks,
                "months": tl.to_months,
                "years": tl.to_years,
                "decades": tl.to_decades,
                "centuries": tl.to_centuries,
            }

        def to_any(self, asked: TimeUnit | str) -> float | timedelta | None:
            dispatch = self._convert_dispatch()
            convert = dispatch.get(asked)
            return convert() if convert else 0.0

        # For a given display unit, which of `_ALL_UNITS` should be kept (i.e. NOT suppressed).
        # "weeks" piggybacks on "days", and "decades"/"centuries" keep "months"/"years" respectively
        # since those pair naturally with them (e.g. "1 decade, 3 months").
        _KEEP_UNIT: dict[str, str] = {
            "microseconds": "microseconds",
            "milliseconds": "milliseconds",
            "seconds": "seconds",
            "minutes": "minutes",
            "hours": "hours",
            "days": "days",
            "weeks": "days",
            "months": "months",
            "years": "years",
            "decades": "months",
            "centuries": "years",
        }

        @staticmethod
        def to_supress(unit: str) -> list[str]:
            """Return every unit that should be suppressed when displaying a duration in `unit`."""
            if unit in {"raw", "time"}:
                return []

            keep = TimeTools._TimeConvert._KEEP_UNIT.get(unit)
            if keep is None:
                return []

            return [u for u in _ALL_UNITS if u != keep]

    _TimeConvert: _TimeConvert
    TimeConvert: _TimeConvert  # NOQA

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
            self.error = asyncio.exceptions.CancelledError
            self.timeout_error = asyncio.exceptions.TimeoutError

        def when(self) -> float | None:
            """Return the current deadline."""
            return self._when

        def reschedule(self, when: float | None) -> None:
            """Reschedule the timeout."""
            if self._state is not _State.ENTERED:
                if self._state is _State.CREATED:
                    raise RuntimeError("Timeout has not been entered")
                raise RuntimeError(f"Cannot change state of {self._state.value} Timeout")

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
            info = [""]
            if self._state is _State.ENTERED:
                when = round(self._when, 3) if self._when is not None else None
                info.append(f"when={when}")
            info_str = " ".join(info)
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
            self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
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

        def duration(self) -> float | int | None:
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
