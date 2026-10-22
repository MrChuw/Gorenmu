from __future__ import annotations

import asyncio
import datetime
import inspect
from collections.abc import Callable
from enum import IntEnum
from typing import Any, Self

from twitchio.backoff import Backoff
from twitchio.ext.routines import LOGGER, CoroT, T  # noqa
from twitchio.ext.routines import Routine as BaseRoutine
from twitchio.ext.routines import routine as base_routine

__all__ = ("Day", "ScheduleBuilder", "Routine", "routine")


class Day(IntEnum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


class Routine(BaseRoutine):
    def __init__(
        self,
        *,
        coro: CoroT,
        slots: list[tuple[Day, datetime.time]] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(coro=coro, **kwargs)
        self._slots: list[tuple[Day, datetime.time]] = slots or []

    def __get__(self, instance: T, type_: type[T]) -> Routine:
        if instance is None:
            return self

        copy = Routine(
            coro=self._coro,
            slots=self._slots,
            name=self._name,
            time=self._time,
            delta=self._original_delta,
            max_attempts=self._max_attempts,
            iterations=self._iterations,
            wait_remainder=self._wait_remainder,
            wait_first=self._wait_first,
            stop_on_error=self._stop_on_error,
        )
        copy._injected = instance
        copy._before_routine = self._before_routine
        copy._after_routine = self._after_routine
        copy._on_error = self._on_error

        setattr(instance, self._coro.__name__, copy)  # ty: ignore[unresolved-attribute]
        return copy

    def _compute_next_run(self, now: datetime.datetime) -> datetime.datetime:
        if not self._slots:
            raise ValueError("No weekly slots scheduled for this routine.")

        candidates: list[datetime.datetime] = []
        for day, time_val in self._slots:
            days_ahead = (day.value - now.weekday()) % 7
            candidate_date = now.date() + datetime.timedelta(days=days_ahead)
            candidate_dt = datetime.datetime.combine(candidate_date, time_val, tzinfo=now.tzinfo)

            if candidate_dt <= now:
                candidate_dt += datetime.timedelta(days=7)

            candidates.append(candidate_dt)

        return min(candidates)

    def next_iteration(self) -> float:
        if self._slots:
            now = datetime.datetime.now(tz=datetime.UTC)
            next_run = self._compute_next_run(now)
            return max((next_run - now).total_seconds(), 0)

        return super().next_iteration()

    async def _routine_loop(self, *args: Any, **kwargs: Any) -> None:
        if not self._slots:
            return await super()._routine_loop(*args, **kwargs)

        backoff = Backoff(base=3, maximum_time=10, maximum_tries=5)

        if self._should_stop:
            return

        if self._before_routine:
            try:
                await self._before_routine(*args, **kwargs)
            except Exception as e:
                await self._call_error(e)
                return self.cancel()

        if self._wait_first:
            await asyncio.sleep(self.next_iteration())

        attempts = self._max_attempts
        try:
            while True:
                self._last_start = datetime.datetime.now(tz=datetime.UTC)
                self._current_iteration += 1

                try:
                    await self._coro(*args, **kwargs)
                except Exception as e:
                    await self._call_error(e)

                    if self._stop_on_error:
                        self._should_stop = False
                        break

                    if attempts is not None:
                        attempts -= 1
                        if attempts <= 0:
                            LOGGER.warning(
                                "The maximum retry attempts for Routine: %s has been reached and will now be canceled.",
                                self.__repr__(),
                            )
                            break

                        await asyncio.sleep(backoff.calculate())
                        continue
                else:
                    attempts = self._max_attempts
                    self._completed += 1

                if self.remaining_iterations is not None and self.remaining_iterations <= 0:
                    break

                if self._should_stop:
                    self._should_stop = False
                    break

                await asyncio.sleep(self.next_iteration())

        except Exception as e:
            LOGGER.error(
                "A fatal error occurred during an iteration of Routine: %s. This routine will now be canceled.",
                self.__repr__(),
                exc_info=e,
            )

        if self._after_routine:
            try:
                await self._after_routine(*args, **kwargs)
            except Exception as e:
                await self._call_error(e)

        self.cancel()


class ScheduleBuilder:
    def __init__(
        self,
        *days: Day,
        name: str | None = None,
        iterations: int | None = None,
        wait_first: bool = True,
        max_attempts: int | None = 5,
        stop_on_error: bool = False,
    ) -> None:
        self._days: set[Day] = set(days)
        self._times: list[datetime.time] = []
        self._config: dict[str, Any] = {
            "name": name,
            "iterations": iterations,
            "wait_first": wait_first,
            "max_attempts": max_attempts,
            "stop_on_error": stop_on_error,
        }

    @staticmethod
    def _parse_time(target: str | datetime.time) -> datetime.time:
        if isinstance(target, datetime.time):
            return target
        parsed = datetime.datetime.strptime(target, "%H:%M")
        return parsed.time()

    # Day properties for chaining
    @property
    def monday(self) -> Self:
        self._days.add(Day.MONDAY)
        return self

    @property
    def tuesday(self) -> Self:
        self._days.add(Day.TUESDAY)
        return self

    @property
    def wednesday(self) -> Self:
        self._days.add(Day.WEDNESDAY)
        return self

    @property
    def thursday(self) -> Self:
        self._days.add(Day.THURSDAY)
        return self

    @property
    def friday(self) -> Self:
        self._days.add(Day.FRIDAY)
        return self

    @property
    def saturday(self) -> Self:
        self._days.add(Day.SATURDAY)
        return self

    @property
    def sunday(self) -> Self:
        self._days.add(Day.SUNDAY)
        return self

    def at(self, *times: str | datetime.time) -> Self:
        for t in times:
            self._times.append(self._parse_time(t))
        return self

    def __call__(self, coro: CoroT) -> Routine:
        if not inspect.iscoroutinefunction(coro):
            raise TypeError(f"Routine expected coroutine function, got {type(coro).__name__!r}")

        if not self._days:
            raise ValueError("ScheduleBuilder requires at least one Day specified.")

        if not self._times:
            raise ValueError("ScheduleBuilder requires at least one target time via .at(...)")

        # Compute cartesian product of days and times
        slots: list[tuple[Day, datetime.time]] = [(day, t) for day in self._days for t in self._times]

        return Routine(
            coro=coro,
            slots=slots,
            time=None,
            delta=None,
            wait_remainder=False,
            **self._config,
        )


class RoutineFactory:
    """Entrypoint namespace preserving TwitchIO defaults while offering the builder."""

    def __call__(
        self,
        *,
        delta: datetime.timedelta | None = None,
        time: datetime.datetime | None = None,
        name: str | None = None,
        iterations: int | None = None,
        wait_first: bool = False,
        wait_remainder: bool = False,
        max_attempts: int | None = 5,
        stop_on_error: bool = False,
    ) -> Callable[[CoroT], BaseRoutine]:
        return base_routine(
            delta=delta,
            time=time,
            name=name,
            iterations=iterations,
            wait_first=wait_first,
            wait_remainder=wait_remainder,
            max_attempts=max_attempts,
            stop_on_error=stop_on_error,
        )

    @staticmethod
    def every(*days: Day, **kwargs: Any) -> ScheduleBuilder:
        return ScheduleBuilder(*days, **kwargs)


routine = RoutineFactory()


"""
# 1. Chaining multiple .at() calls on a single property
@routine.every().friday.at("12:00").at("18:00")
async def single_day_chained() -> None:
    pass

# 2. Passing multiple times in a single .at() call
@routine.every().friday.at("12:00", "18:00")
async def single_day_multi_arg() -> None:
    pass

# 3. Chaining properties across multiple days
@routine.every().tuesday.thursday.at("12:00", "18:00")
async def multi_day_properties() -> None:
    pass

# 4. Supplying Day Enums directly into .every()
@routine.every(Day.TUESDAY, Day.THURSDAY).at("12:00", "18:00")
async def multi_day_enums() -> None:
    pass

# 5. Default TwitchIO routine syntax remains untouched
@routine(delta=datetime.timedelta(minutes=5))
async def standard_routine() -> None:
    pass
"""
