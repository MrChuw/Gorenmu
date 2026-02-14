from __future__ import annotations

import asyncio
import contextlib
import heapq
from collections import deque
from datetime import timedelta
from typing import TYPE_CHECKING, Any

NumberOrDelta = float | int | timedelta

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class AcquireTimeoutError(asyncio.TimeoutError):
    """Raised when acquire() times out waiting for a slot."""


def _to_seconds(value: NumberOrDelta | None) -> float | None:
    """Convert float/int/timedelta to seconds (float). Returns None if value is None."""
    if value is None:
        return None
    return value.total_seconds() if isinstance(value, timedelta) else float(value)


class AdvancedSemaphore:
    """
    An advanced concurrency primitive that combines:
      - concurrency limit (like a normal semaphore)
      - burst control (token-bucket style)
      - ramp-up (staggering / token production rate)
      - cooldown after release (pushes next allowed entry forward)
      - acquire timeout (so waiters don't live forever)
      - priority queue for waiters (lower number == higher priority)
      - circuit-breaker behavior: trip when failures exceed threshold in a sliding window
      - sliding window rate limit (max_per_window / window_seconds)
      - telemetry/metrics and Prometheus export helper (user must call to collect)
    """

    def __init__(
        self,
        name: str,
        limit: int,
        ramp_up: NumberOrDelta = 0.0,
        cooldown: NumberOrDelta = 0.0,
        burst_size: int = 0,
        acquire_timeout: NumberOrDelta | None = None,
        max_per_window: int | None = None,
        window_seconds: NumberOrDelta = 60,
        failure_threshold: int | None = None,
        failure_window: NumberOrDelta = 60.0,
        auto_recovery_timeout: NumberOrDelta = 30.0,
        metrics_history: int = 1000,
    ):
        """
        Initialize the AdvancedSemaphore.

        Args:
            name: logical name for metrics/logging.
            limit: maximum concurrent holders.
            ramp_up: time between token production (seconds or timedelta).
                If 0, tokens refill instantly up to burst_size.
            cooldown: extra seconds pushed to next allowed entry on release.
            burst_size: how many tokens can accumulate for an initial burst.
            acquire_timeout: default timeout for acquire (seconds or timedelta); None means wait forever.
            max_per_window: optional max allowed entries in the sliding window (window_seconds).
            window_seconds: length of sliding window for rate-limiting (seconds or timedelta).
            failure_threshold: number of failures in failure_window to trip circuit.
            failure_window: sliding window (seconds or timedelta) for failure counting.
            auto_recovery_timeout: seconds (or timedelta) to auto-resume after tripping.
            metrics_history: how many wait-times to keep for averaging.
        """
        self.name = name

        # concurrency
        self._limit = limit
        self._value = 0

        # waiters as min-heap of (priority, seq, future)
        self._waiters_heap = []
        self._waiters_seq = 0

        # knobs (store as seconds where applicable)
        self._ramp_up = _to_seconds(ramp_up) or 0.0
        self._cooldown = _to_seconds(cooldown) or 0.0
        self._burst_size = burst_size
        self._acquire_timeout_default = _to_seconds(acquire_timeout)
        self._max_per_window = int(max_per_window) if max_per_window is not None else None
        self._window_seconds = int(_to_seconds(window_seconds) or 60)

        # token-bucket state
        self._tokens = float(self._burst_size)
        self._last_token_time = asyncio.get_running_loop().time()

        # scheduling control
        self._next_allowed_entry = 0.0
        self._entry_lock = asyncio.Lock()

        # circuit breaker
        self._paused = False
        self._failure_threshold = int(failure_threshold) if failure_threshold is not None else None
        self._failure_window = _to_seconds(failure_window) or 60.0
        self._auto_recovery_timeout = _to_seconds(auto_recovery_timeout) or 30.0
        self._failure_timestamps = deque()

        # rate window timestamps (when entries were granted)
        self._entry_timestamps = deque()

        # metrics
        self._waiting_times = deque(maxlen=metrics_history)
        self._wait_start_times: dict[asyncio.Future, float] = {}
        now = asyncio.get_running_loop().time()
        self._start_time = now
        self._last_value_change_time = now
        self._full_time_accumulator = 0.0  # accumulated time while at full capacity
        self._total_acquired_count = 0
        self._total_releases = 0
        self._total_time_inside = 0.0
        self._active_entry_timestamps = deque()  # timestamps when a slot was granted (FIFO)
        self._peak_concurrency = 0
        self._max_wait_time = 0.0
        self._min_wait_time: float | None = None

        # scheduling control
        self._next_allowed_entry = 0.0
        self._entry_lock = asyncio.Lock()
        # wake scheduler handle (used to wake waiters when tokens/time become available)
        self._wake_handle: asyncio.Handle | None = None

    # --------------------------
    # Basic properties & helpers
    # --------------------------
    @property
    def limit(self) -> int:
        """Current configured concurrency limit."""
        return self._limit

    @property
    def locked(self) -> bool:
        """True if semaphore is paused or currently at/above limit."""
        return self._paused or (self._value >= self._limit)

    def _update_full_accumulator_on_change(self, prev_value: int, new_value: int) -> None:
        """
        Update accumulated 'full' time whenever the concurrency count changes.
        Called from places that change _value.
        """
        now = asyncio.get_running_loop().time()
        if prev_value >= self._limit:
            # previously full -> add elapsed time
            self._full_time_accumulator += now - self._last_value_change_time
        self._last_value_change_time = now
        # update peak concurrency
        if new_value > self._peak_concurrency:
            self._peak_concurrency = new_value

    def _refill_tokens(self) -> None:
        """
        Refill token-bucket based on elapsed time and ramp_up.
        A token is considered produced every `ramp_up` seconds. If ramp_up==0,
        tokens are instantly set to burst_size (no pacing).
        """
        now = asyncio.get_running_loop().time()
        if self._ramp_up <= 0:
            self._tokens = float(self._burst_size)
            self._last_token_time = now
            return
        elapsed = now - self._last_token_time
        if elapsed <= 0:
            return
        produced = elapsed / self._ramp_up
        if produced > 0:
            self._tokens = min(float(self._burst_size), self._tokens + produced)
            self._last_token_time = now

    # --------------------------
    # Acquire / Release
    # --------------------------
    async def acquire(self, priority: int = 10, timeout: NumberOrDelta | None = None) -> bool:
        """
        Acquire a slot.

        Args:
            priority: lower numbers have higher priority (default 10).
            timeout: optional override for this acquire call; accepts float/int (seconds) or timedelta.
                     If None, uses the semaphore's default timeout (which itself may be None = wait forever).

        Returns:
            True on successful acquire.

        Raises:
            AcquireTimeoutError if the wait times out.
        """
        eff_timeout = _to_seconds(timeout) if timeout is not None else self._acquire_timeout_default
        start_wait = asyncio.get_running_loop().time()
        fut = None

        while True:
            async with self._entry_lock:
                # circuit paused?
                paused_now = self._paused

                # refill tokens
                self._refill_tokens()

                # enforce sliding rate window
                now = asyncio.get_running_loop().time()
                cutoff = now - self._window_seconds
                while self._entry_timestamps and self._entry_timestamps[0] <= cutoff:
                    self._entry_timestamps.popleft()
                exceeded_window = (
                    self._max_per_window is not None and len(self._entry_timestamps) >= self._max_per_window
                )

                # compute immediate entry eligibility
                next_slot_allowed = max(now, self._next_allowed_entry)
                token_available = self._tokens >= 1.0
                within_concurrency = self._value < self._limit
                can_enter_immediately = (
                    not paused_now
                    and within_concurrency
                    and not exceeded_window
                    and token_available
                    and next_slot_allowed <= now
                )

                if can_enter_immediately:
                    # grant immediate slot
                    self._tokens -= 1.0
                    prev = self._value
                    self._value += 1
                    self._total_acquired_count += 1
                    self._entry_timestamps.append(now)
                    self._active_entry_timestamps.append(now)
                    if self._ramp_up > 0:
                        self._next_allowed_entry = now + self._ramp_up
                        self._last_token_time = now
                    self._update_full_accumulator_on_change(prev, self._value)
                    # wait time 0
                    self._waiting_times.append(0.0)
                    # update min/max wait metrics
                    if self._min_wait_time is None or self._min_wait_time > 0.0:
                        self._min_wait_time = 0.0
                    # update peak
                    if self._value > self._peak_concurrency:
                        self._peak_concurrency = self._value
                    return True

                # cannot enter now: enqueue as waiter if not already
                if fut is None:
                    # fut = asyncio.get_running_loop().create_future()
                    # self._wait_start_times[fut] = start_wait
                    # heapq.heappush(self._waiters_heap, (priority, self._waiters_seq, fut))
                    # self._waiters_seq += 1
                    # enqueue waiter
                    fut = asyncio.get_running_loop().create_future()
                    self._wait_start_times[fut] = start_wait
                    heapq.heappush(self._waiters_heap, (priority, self._waiters_seq, fut))
                    self._waiters_seq += 1

                    # ---- schedule a wake for the earliest reason a slot may open ----
                    # compute delays to next token / next allowed entry / rate-window expiry
                    now = asyncio.get_running_loop().time()
                    delays: list[float] = []

                    # token-based wake (if token not available and ramp_up > 0)
                    if not token_available and self._ramp_up > 0 and self._burst_size > 0:
                        missing = max(0.0, 1.0 - self._tokens)
                        if missing > 0:
                            delays.append(missing * self._ramp_up)

                    # next slot allowed (ramp_up / cooldown)
                    if next_slot_allowed > now:
                        delays.append(next_slot_allowed - now)

                    # rate-window expiry (if exceeded)
                    if exceeded_window and self._entry_timestamps:
                        oldest = self._entry_timestamps[0]
                        wait_needed = (oldest + self._window_seconds) - now
                        if wait_needed > 0:
                            delays.append(wait_needed)

                    # choose earliest positive delay
                    delay = min(delays) if delays else None
                    if delay is not None:
                        # schedule wake so waiters get a chance to re-check when tokens/time allow
                        self._schedule_wake(delay)

            # Outside lock: wait for fut to be completed or timeout/cancel
            try:
                if eff_timeout is None:
                    await fut
                else:
                    await asyncio.wait_for(fut, timeout=eff_timeout)
            except TimeoutError as e:
                # mark/cleanup waiter
                async with self._entry_lock:
                    if not fut.done():
                        fut.cancel()
                    waited = asyncio.get_running_loop().time() - self._wait_start_times.pop(fut, start_wait)
                    self._waiting_times.append(waited)
                    self._max_wait_time = max(self._max_wait_time, waited)
                    if self._min_wait_time is None or waited < self._min_wait_time:
                        self._min_wait_time = waited
                raise AcquireTimeoutError(f"acquire timeout after {eff_timeout}s") from e
            except asyncio.CancelledError:
                async with self._entry_lock:
                    waited = asyncio.get_running_loop().time() - self._wait_start_times.pop(fut, start_wait)
                    self._waiting_times.append(waited)
                    self._max_wait_time = max(self._max_wait_time, waited)
                    if self._min_wait_time is None or waited < self._min_wait_time:
                        self._min_wait_time = waited
                raise

            # fut completed -> record waited time
            # (we may be woken up even if another waiter got the slot; we loop and re-check)
            if fut in self._wait_start_times:
                waited = asyncio.get_running_loop().time() - self._wait_start_times.pop(fut, start_wait)
                self._waiting_times.append(waited)
                self._max_wait_time = max(self._max_wait_time, waited)
                if self._min_wait_time is None or waited < self._min_wait_time:
                    self._min_wait_time = waited
            # loop continues and re-checks conditions to actually acquire (the waiter is signalled to re-check)

    def release(self) -> None:
        """
        Release a previously acquired slot.

        Notes:
            - This method does NOT attempt to verify that the caller actually holds a slot.
            - On release we compute an approximate 'time inside' metric by pairing releases with the earliest
              active entry timestamp (FIFO). This is an approximation of per-task time-inside.
        """
        prev_val = self._value
        self._value = max(0, self._value - 1)
        self._total_releases += 1

        # compute time-inside if we have a matching acquire timestamp
        now = asyncio.get_running_loop().time()
        if self._active_entry_timestamps:
            start_ts = self._active_entry_timestamps.popleft()
            elapsed = max(0.0, now - start_ts)
            self._total_time_inside += elapsed

        self._update_full_accumulator_on_change(prev_val, self._value)

        # cooldown pushes next allowed entry forward
        if self._cooldown > 0:
            current_target = max(now, self._next_allowed_entry)
            self._next_allowed_entry = current_target + self._cooldown

        # attempt to wake a waiter
        self._wake_up_next()

    def _wake_up_next(self) -> None:
        """
        Try to wake the highest-priority waiter (non-blocking). Uses entry_lock to manipulate the heap.
        We schedule an async helper as this may be called from non-async contexts.
        """
        self._cancel_scheduled_wake()

        async def _async_wake():
            async with self._entry_lock:
                self._refill_tokens()
                now = asyncio.get_running_loop().time()

                cutoff = now - self._window_seconds
                while self._entry_timestamps and self._entry_timestamps[0] <= cutoff:
                    self._entry_timestamps.popleft()

                exceeded_window = (
                    self._max_per_window is not None and len(self._entry_timestamps) >= self._max_per_window
                )

                while self._waiters_heap:
                    prio, seq, fut = heapq.heappop(self._waiters_heap)

                    if fut.done():
                        continue

                    can_enter = (
                        not self._paused
                        and self._value < self._limit
                        and self._tokens >= 1.0
                        and not exceeded_window
                        and self._next_allowed_entry <= now
                    )

                    if not can_enter:
                        heapq.heappush(self._waiters_heap, (prio, seq, fut))

                        delays = []

                        if self._tokens < 1.0 and self._ramp_up > 0 and self._burst_size > 0:
                            missing = 1.0 - self._tokens
                            delays.append(missing * self._ramp_up)

                        if self._next_allowed_entry > now:
                            delays.append(self._next_allowed_entry - now)

                        if exceeded_window and self._entry_timestamps:
                            oldest = self._entry_timestamps[0]
                            delays.append((oldest + self._window_seconds) - now)

                        if delays:
                            self._schedule_wake(min(d for d in delays if d > 0))

                        break
                    fut.set_result(True)
                    break

        with contextlib.suppress(RuntimeError):
            loop = asyncio.get_running_loop()
            loop.create_task(_async_wake())  # NOQA: RUF006

    def _cancel_scheduled_wake(self) -> None:
        """Cancel previously scheduled wake if exists."""
        if getattr(self, "_wake_handle", None) is not None:
            with contextlib.suppress(Exception):
                self._wake_handle.cancel()
            self._wake_handle = None

    def _schedule_wake(self, delay: float) -> None:
        """
        Schedule a wake call after `delay` seconds to re-check tokens/slots and wake waiters.
        Only keeps one scheduled handle (cancels previous).
        """
        # small negative/zero guard
        if delay is None:
            return
        if delay <= 0:
            # immediate: wake now (non-blocking)
            self._wake_up_next()
            return
        # avoid scheduling absurdly long timers
        loop = asyncio.get_running_loop()
        self._cancel_scheduled_wake()
        # schedule _wake_up_next to run in the loop after `delay`.
        # _wake_up_next itself will create a task to run the async wake logic.
        self._wake_handle = loop.call_later(delay, self._wake_up_next)

    # --------------------------
    # Context manager
    # --------------------------
    async def __aenter__(self):
        """Async context manager entry -> acquires a slot."""
        await self.acquire()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        """
        Async context manager exit -> records success/failure and releases.
        Note: returns False so exceptions propagate.
        """
        if exc_type is None:
            self.record_success()
        else:
            self.record_failure()
        self.release()
        return False

    # --------------------------
    # Circuit breaker / failure tracking
    # --------------------------
    def record_failure(self) -> None:
        """
        Register a failure observed by a task that used the semaphore.
        If failure_threshold is set and exceeded within failure_window, the semaphore is paused
        and will auto-resume after auto_recovery_timeout.
        """
        now = asyncio.get_running_loop().time()
        self._failure_timestamps.append(now)
        cutoff = now - self._failure_window
        while self._failure_timestamps and self._failure_timestamps[0] <= cutoff:
            self._failure_timestamps.popleft()
        if self._failure_threshold is not None and len(self._failure_timestamps) >= self._failure_threshold:
            self._trip_circuit()

    def record_success(self) -> None:
        """Register a success. Purges old failure timestamps."""
        now = asyncio.get_running_loop().time()
        cutoff = now - self._failure_window
        while self._failure_timestamps and self._failure_timestamps[0] <= cutoff:
            self._failure_timestamps.popleft()

    def _trip_circuit(self) -> None:
        """Trip the circuit (pause) and schedule an auto-resume."""
        if self._paused:
            return
        self._paused = True
        loop = asyncio.get_running_loop()
        loop.call_later(self._auto_recovery_timeout, self.resume)  # NOQA

    def pause(self) -> None:
        """Pause the semaphore immediately (no new entries until resumed)."""
        self._paused = True

    def resume(self) -> None:
        """Resume the semaphore and attempt to wake waiters."""
        self._paused = False
        self._wake_up_next()

    # --------------------------
    # Dynamic configuration
    # --------------------------
    def configure(self, **kwargs) -> None:
        """
        Update knobs at runtime. Supported keys:
          - limit (int)
          - ramp_up (seconds or timedelta)
          - cooldown (seconds or timedelta)
          - burst_size (int)
          - acquire_timeout (seconds or timedelta or None)
          - max_per_window (int or None)
          - window_seconds (seconds or timedelta)
          - failure_threshold (int or None)
          - failure_window (seconds or timedelta)
          - auto_recovery_timeout (seconds or timedelta)
        NOTE: changing 'limit' will NOT cancel or kill currently running holders. If you lower the limit
              below the current number of holders, running holders continue until they release; new
              acquisitions will be blocked until the count drops below the new limit.
        """
        allowed = {
            "limit",
            "ramp_up",
            "cooldown",
            "burst_size",
            "acquire_timeout",
            "max_per_window",
            "window_seconds",
            "failure_threshold",
            "failure_window",
            "auto_recovery_timeout",
        }
        for k, v in kwargs.items():
            if k not in allowed:
                continue
            if k == "limit":
                old = self._limit
                self._limit = int(v)
                # If increased, wake waiters immediately
                if self._limit > old:
                    self._wake_up_next()
            elif k == "ramp_up":
                self._ramp_up = _to_seconds(v) or 0.0
            elif k == "cooldown":
                self._cooldown = _to_seconds(v) or 0.0
            elif k == "burst_size":
                self._burst_size = int(v)
                self._tokens = min(self._tokens, float(self._burst_size))
            elif k == "acquire_timeout":
                self._acquire_timeout_default = _to_seconds(v)
            elif k == "max_per_window":
                self._max_per_window = None if v is None else int(v)
            elif k == "window_seconds":
                self._window_seconds = int(_to_seconds(v) or 60)
            elif k == "failure_threshold":
                self._failure_threshold = None if v is None else int(v)
            elif k == "failure_window":
                self._failure_window = _to_seconds(v) or 60.0
            elif k == "auto_recovery_timeout":
                self._auto_recovery_timeout = _to_seconds(v) or 30.0

    # --------------------------
    # Metrics & Prometheus helper
    # --------------------------
    def waiting_count(self) -> int:
        """Return how many waiters are currently pending (approximate; excludes done/cancelled)."""
        return sum(not fut.done() for _, _, fut in self._waiters_heap)

    def average_wait_time(self) -> float:
        """Average of recorded wait times (seconds)."""
        if not self._waiting_times:
            return 0.0
        return sum(self._waiting_times) / len(self._waiting_times)

    def average_time_inside(self) -> float:
        """Average time tasks spent inside (seconds), based on recorded acquisitions/releases."""
        if self._total_releases == 0:
            return 0.0
        return self._total_time_inside / self._total_releases

    def utilization_rate(self) -> float:
        """
        Fraction of time (0..1) the semaphore spent at full capacity since creation.
        This uses start_time, full_time_accumulator and in-flight time if currently full.
        """
        now = asyncio.get_running_loop().time()
        acc = self._full_time_accumulator
        if self._value >= self._limit:
            acc += now - self._last_value_change_time
        elapsed = max(1e-9, now - self._start_time)
        return acc / elapsed

    def export_metrics(self) -> dict[str, Any]:
        """Return a dict with current metrics (suitable for JSON export)."""
        return {
            "name": self.name,
            "waiting_count": self.waiting_count(),
            "average_wait_time": self.average_wait_time(),
            "max_wait_time": self._max_wait_time,
            "min_wait_time": self._min_wait_time or 0.0,
            "utilization_rate": self.utilization_rate(),
            "current_value": self._value,
            "limit": self._limit,
            "paused": self._paused,
            "burst_tokens": self._tokens,
            "recent_failures": len(self._failure_timestamps),
            "entries_in_window": len(self._entry_timestamps),
            "total_acquired_count": self._total_acquired_count,
            "total_releases": self._total_releases,
            "average_time_inside": self.average_time_inside(),
            "peak_concurrency": self._peak_concurrency,
        }

    def prometheus_metrics(self, prefix: str = "advanced_semaphore") -> str:
        """
        Build Prometheus text exposition lines for important metrics.
        This function RETURNS the text; it does not push to anywhere (you will call it when you want to scrape/push).

        Args:
            prefix: metric name prefix (default "advanced_semaphore").

        Returns:
            A string with several newline-separated Prometheus metric lines.
        """
        m = self.export_metrics()
        # gauges
        lines = [
            f"# HELP {prefix}_waiting_count Number of waiters pending for the semaphore.",
            f"# TYPE {prefix}_waiting_count gauge",
            f'{prefix}_waiting_count{{name="{self.name}"}} {m["waiting_count"]}',
            f"# HELP {prefix}_current_value Current concurrent holders.",
            f"# TYPE {prefix}_current_value gauge",
            f'{prefix}_current_value{{name="{self.name}"}} {m["current_value"]}',
            f"# HELP {prefix}_limit Configured concurrency limit.",
            f"# TYPE {prefix}_limit gauge",
            f'{prefix}_limit{{name="{self.name}"}} {m["limit"]}',
            f"# HELP {prefix}_utilization Fraction of time at full utilization [0..1].",
            f"# TYPE {prefix}_utilization gauge",
            f'{prefix}_utilization{{name="{self.name}"}} {m["utilization_rate"]}',
            f"# HELP {prefix}_average_wait_time Average wait time in seconds.",
            f"# TYPE {prefix}_average_wait_time gauge",
            f'{prefix}_average_wait_time{{name="{self.name}"}} {m["average_wait_time"]}',
            f"# HELP {prefix}_average_time_inside Average time inside (seconds).",
            f"# TYPE {prefix}_average_time_inside gauge",
            f'{prefix}_average_time_inside{{name="{self.name}"}} {m["average_time_inside"]}',
            f"# HELP {prefix}_peak_concurrency Peak concurrent holders observed.",
            f"# TYPE {prefix}_peak_concurrency gauge",
            f'{prefix}_peak_concurrency{{name="{self.name}"}} {m["peak_concurrency"]}',
            f"# HELP {prefix}_recent_failures Number of failures in failure window.",
            f"# TYPE {prefix}_recent_failures gauge",
            f'{prefix}_recent_failures{{name="{self.name}"}} {m["recent_failures"]}',
        ]

        return "\n".join(lines) + "\n"

    # --------------------------
    # Convenience status/query
    # --------------------------
    def waiting_list_snapshot(self) -> list:
        """Return a snapshot list of waiter priorities & seq (debugging)."""
        return [(p, s) for (p, s, f) in self._waiters_heap]

    # --------------------------
    # End of class AdvancedSemaphore
    # --------------------------


class SemaphoreManager:
    """
    Manager for multiple AdvancedSemaphore instances. Provides convenience methods to create,
    fetch, update knobs, and perform quick operations on specific semaphores.
    """

    def __init__(self, bot: Gorenmu):
        self.bot: Gorenmu = bot
        self._semaphores: dict[str, AdvancedSemaphore] = {}

    def get_semaphore(
        self,
        name: str,
        *,
        limit: int = 50,
        ramp_up: float | int | timedelta = 0.0,
        cooldown: float | int | timedelta = 0.0,
        burst_size: int = 1,
        acquire_timeout: float | int | timedelta | None = None,
        max_per_window: int | None = None,
        window_seconds: float | int | timedelta = 0,
        failure_threshold: int | None = None,
        failure_window: float | int | timedelta = 60.0,
        auto_recovery_timeout: float | int | timedelta = 30.0,
    ) -> AdvancedSemaphore:
        """
        Return an existing semaphore by name or create a new one.

        Parameters
        ----------
        name : str
            Unique semaphore identifier.

        limit : int
            Maximum number of concurrent holders.

        ramp_up : float | int | timedelta
            Delay between consecutive entries (staggering).

        cooldown : float | int | timedelta
            Extra delay applied after release before allowing next entry.

        burst_size : int
            Number of immediate entries allowed before ramp-up starts.

        acquire_timeout : float | int | timedelta | None
            Maximum time a task can wait in queue before raising TimeoutError.

        max_per_window : int | None
            Maximum number of successful acquisitions allowed per time window.

        window_seconds : float | int | timedelta
            Duration of the rate-limit window.

        failure_threshold : int | None
            Number of failures within `failure_window` required to trigger circuit breaker.

        failure_window : float | int | timedelta
            Time window used to count failures for circuit breaker.

        auto_recovery_timeout : float | int | timedelta
            Time the semaphore stays paused after circuit breaker triggers.

        Returns
        -------
        AdvancedSemaphore
            The existing or newly created semaphore instance.
        """

        if name not in self._semaphores:
            sem = AdvancedSemaphore(
                name=name,
                limit=limit,
                ramp_up=ramp_up,
                cooldown=cooldown,
                burst_size=burst_size,
                acquire_timeout=acquire_timeout,
                max_per_window=max_per_window,
                window_seconds=window_seconds,
                failure_threshold=failure_threshold,
                failure_window=failure_window,
                auto_recovery_timeout=auto_recovery_timeout,
            )
            self._semaphores[name] = sem

        return self._semaphores[name]

    def update_knobs(self, name: str, **kwargs) -> None:
        """Generic knob update (calls configure on the semaphore)."""
        if name in self._semaphores:
            self._semaphores[name].configure(**kwargs)

    # convenience specific updaters:
    def update_limit(self, name: str, limit: int) -> None:
        """Update concurrency limit for semaphore `name` (will not kill running tasks)."""
        if name in self._semaphores:
            self._semaphores[name].configure(limit=limit)

    def update_cooldown(self, name: str, cooldown: NumberOrDelta) -> None:
        if name in self._semaphores:
            self._semaphores[name].configure(cooldown=cooldown)

    def update_burst(self, name: str, burst_size: int) -> None:
        if name in self._semaphores:
            self._semaphores[name].configure(burst_size=burst_size)

    def update_ramp_up(self, name: str, ramp_up: NumberOrDelta) -> None:
        if name in self._semaphores:
            self._semaphores[name].configure(ramp_up=ramp_up)

    def update_acquire_timeout(self, name: str, timeout: NumberOrDelta | None) -> None:
        if name in self._semaphores:
            self._semaphores[name].configure(acquire_timeout=timeout)

    def update_max_per_window(
        self, name: str, max_per_window: int | None, window_seconds: NumberOrDelta | None = None
    ) -> None:
        if name in self._semaphores:
            kwargs = {"max_per_window": max_per_window}
            if window_seconds is not None:
                kwargs["window_seconds"] = window_seconds
            self._semaphores[name].configure(**kwargs)

    def pause(self, name: str) -> None:
        """Pause a semaphore by name."""
        if name in self._semaphores:
            self._semaphores[name].pause()

    def pause_all(self) -> None:
        """
        Pause all managed semaphores.

        While paused, no new acquisitions will be allowed, but
        already running tasks are NOT interrupted.
        """
        for sem in self._semaphores.values():
            sem.pause()

    def resume_all(self) -> None:
        """
        Resume all managed semaphores after a global pause.

        Waiting tasks may proceed normally again.
        """
        for sem in self._semaphores.values():
            sem.resume()

    def resume(self, name: str) -> None:
        """Resume a paused semaphore by name."""
        if name in self._semaphores:
            self._semaphores[name].resume()

    def list_semaphores(self) -> list:
        """Return list of semaphore names currently managed."""
        return list(self._semaphores.keys())

    def remove_semaphore(self, name: str) -> None:
        """Remove semaphore from manager (does not attempt to stop running tasks)."""
        if name in self._semaphores:
            del self._semaphores[name]

    def get_metrics(self, name: str) -> dict[str, Any] | None:
        """Return exported metrics dict for the named semaphore or None if not found."""
        sem = self._semaphores.get(name)
        return None if sem is None else sem.export_metrics()

    def prometheus_metrics(self, name: str, prefix: str = "advanced_semaphore") -> str | None:
        """Return Prometheus text metrics for the semaphore (or None if not found)."""
        sem = self._semaphores.get(name)
        return None if sem is None else sem.prometheus_metrics(prefix=prefix)
