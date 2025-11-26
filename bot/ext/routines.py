import asyncio
import datetime
from collections.abc import Callable

from twitchio.ext.routines import Routine as BaseRoutine
from twitchio.ext.routines import compute_timedelta

__all__ = "Routine"


# TODO: Remake everything based on new routines


class Routine(BaseRoutine):
    def __init__(
        self,
        *,
        coro: Callable,
        loop: asyncio.AbstractEventLoop | None = None,
        iterations: int | None = None,
        time: datetime.datetime | None = None,
        delta: float | None = None,
        wait_first: bool | None = False,
        weekly_days: list[int] | None = None,
        weekly_times: list[datetime.time] | None = None,
    ):
        self._coro = coro
        self._loop = loop or asyncio.get_event_loop()
        self._task: asyncio.Task = None  # type: ignore

        self._time = time
        self._delta = delta

        self._start_time: datetime.datetime = None  # type: ignore

        self._completed_loops = 0

        iterations = iterations if iterations != 0 else None
        self._iterations = iterations
        self._remaining_iterations = iterations

        self._before = None
        self._after = None
        self._error = None

        self._stop_set = False
        self._restarting = False
        self._wait_first = wait_first

        self._stop_on_error = True

        self._instance = None

        self._args: tuple | None = None
        self._kwargs: dict | None = None

        self._weekly_days = weekly_days
        self.weekly_times = weekly_times

    async def _routine(self, *args, **kwargs) -> None:
        self._stop_on_error = kwargs.pop("stop_on_error", self._stop_on_error)

        self._start_time = datetime.datetime.now(datetime.UTC)

        try:
            if self._before:
                if self._instance:
                    await self._before(self._instance)
                else:
                    await self._before()
        except Exception as e:
            await self._error(e)

            if self._stop_on_error:
                return self.cancel()

        if self._weekly_days and self.weekly_times:
            while True:
                if self._iterations is not None and self._remaining_iterations <= 0:
                    break

                now = datetime.datetime.now()
                next_run = self._compute_next_weekly_run(now)
                await asyncio.sleep((next_run - now).total_seconds())
                await self._execute_routine(args, kwargs)

                # Update remaining iterations
                if self._iterations is not None:
                    self._remaining_iterations -= 1
        else:
            if self._time:
                wait = compute_timedelta(self._time)
                await asyncio.sleep(wait)

            if self._wait_first and not self._time:
                await asyncio.sleep(self._delta)

            if self._remaining_iterations == 0:
                self._remaining_iterations = self._iterations

            iteration: int = 0
            while True:
                iteration += 1
                start = datetime.datetime.now(datetime.UTC)

                await self._execute_routine(args, kwargs)

                try:
                    self._remaining_iterations -= 1
                except TypeError:
                    pass
                else:
                    if self._remaining_iterations == 0:
                        break

                if self._stop_set:
                    self._stop_set = False
                    break

                if self._time:
                    sleep = compute_timedelta(self._time + datetime.timedelta(days=iteration))
                else:
                    sleep = max(
                        (start - datetime.datetime.now(datetime.UTC)).total_seconds() + self._delta,
                        0,
                    )

                self._completed_loops += 1
                await asyncio.sleep(sleep)

        try:
            if self._after:
                if self._instance:
                    await self._after(self._instance)
                else:
                    await self._after()
        except Exception as e:
            await self._error(e)
        finally:
            return self.cancel()  # NOQA: B012

    def _compute_next_weekly_run(self, now: datetime.datetime) -> datetime.datetime:
        """Compute the next run time based on weekly_days and weekly_time."""
        next_run = None
        for day, time in zip(self._weekly_days, self.weekly_times, strict=False):
            next_run_candidate = now + datetime.timedelta((day - now.weekday() + 7) % 7)
            next_run_candidate = datetime.datetime.combine(next_run_candidate.date(), time)
            if next_run_candidate > now and (next_run is None or next_run_candidate < next_run):
                next_run = next_run_candidate
        if next_run is None:
            next_run = datetime.datetime.combine(now.date() + datetime.timedelta(7), self.weekly_times[0])
        return next_run

    async def _execute_routine(self, args, kwargs) -> None:
        try:
            if self._instance:
                await self._coro(self._instance, *args, **kwargs)
            else:
                await self._coro(*args, **kwargs)
        except Exception as e:
            await self._error(e)

            if self._stop_on_error:
                return self.cancel()


def routine(
    *,
    seconds: float | None = 0,
    minutes: float | None = 0,
    hours: float | None = 0,
    time: datetime.datetime | None = None,
    iterations: int | None = None,
    wait_first: bool | None = False,
    weekly_days: list[int] | None = None,  # Lista de dias da semana
    weekly_times: list[datetime.time] | None = None,  # Lista de horários
):
    def decorator(coro: Callable) -> Routine:
        time_ = time
        weekly_time = weekly_times
        if any((seconds, minutes, hours)) and time_:
            raise RuntimeError(
                "Argument <time> cannot be used in conjunction with any <seconds>, <minutes> or <hours> argument(s)."
            )

        if weekly_days and weekly_times:
            if not isinstance(weekly_days, list) or not all(
                isinstance(day, int) and 0 <= day <= 6 for day in weekly_days
            ):
                raise TypeError("weekly_days must be a list of integers between 0 and 6.")
            if not isinstance(weekly_time, list) or not all(isinstance(t, datetime.time) for t in weekly_time):
                raise TypeError("weekly_time must be a list of datetime.time objects.")

            if len(weekly_time) < len(weekly_days):
                weekly_time += [datetime.time(hour=12, minute=0)] * (len(weekly_days) - len(weekly_time))
            elif len(weekly_time) > len(weekly_days):
                weekly_time = weekly_time[: len(weekly_days)]

            delta = None
        else:
            if not time_:
                delta = compute_timedelta(
                    datetime.datetime.now(datetime.UTC)
                    + datetime.timedelta(seconds=seconds, minutes=minutes, hours=hours)
                )
            else:
                delta = None
                now = datetime.datetime.now(time_.tzinfo)
                if time_ < now:
                    time_ = datetime.datetime.combine(now.date(), time_.time())
                if time_ < now:
                    time_ = time_ + datetime.timedelta(days=1)

        if not asyncio.iscoroutinefunction(coro):
            raise TypeError(f"Expected coroutine function, not type {type(coro).__name__!r}.")

        return Routine(
            coro=coro,
            time=time_,
            delta=delta,
            iterations=iterations,
            wait_first=wait_first,
            weekly_days=weekly_days,
            weekly_times=weekly_time,
        )

    return decorator
