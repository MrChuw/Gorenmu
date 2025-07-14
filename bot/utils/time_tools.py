import asyncio
import re
from datetime import datetime, timedelta


class TimeTools:
    def __init__(self): ...

    @staticmethod
    def _parse_duration(text: str) -> timedelta | None:
        """
        Parse duration strings like '2h 30m', '1d 4h', etc. into a timedelta object.
        Supported units: weeks (w), days (d), hours (h), minutes (m), seconds (s).
        """
        pattern = re.compile(
            r"""
            (?:(?P<years>\d+)\s*(?:years?|yrs?|y))?\s*
            (?:(?P<months>\d+)\s*(?:months?|mos?|mo))?\s*
            (?:(?P<weeks>\d+)\s*(?:weeks?|w))?\s*
            (?:(?P<days>\d+)\s*(?:days?|d))?\s*
            (?:(?P<hours>\d+)\s*(?:hours?|hrs?|h))?\s*
            (?:(?P<minutes>\d+)\s*(?:minutes?|mins?|m))?\s*
            (?:(?P<seconds>\d+)\s*(?:seconds?|secs?|s))?
            """,
            re.IGNORECASE | re.VERBOSE,
        )

        match = pattern.fullmatch(text.strip())
        if not match:
            return None

        gd = match.groupdict(default="0")
        # Approximate years = 365 days, months = 30 days
        days = int(gd["years"]) * 365 + int(gd["months"]) * 30 + int(gd["weeks"]) * 7 + int(gd["days"])
        hours = int(gd["hours"])
        minutes = int(gd["minutes"])
        seconds = int(gd["seconds"])

        return timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

    @staticmethod
    def _parse_datetime_with_date(text: str) -> datetime | None:
        """
        Parse date strings in formats like:
        - '12/06/2025'
        - '12/06/2025 14:30'
        - '14:30 12/06/2025'
        Returns a datetime object or None.
        """
        pattern1 = re.compile(
            r"""
            \b
            (?P<day>\d{1,2})/(?P<month>\d{1,2})/(?P<year>\d{2,4})
            (?:\s+
                (?P<hour>\d{1,2}):(?P<minute>\d{2})
                (?::(?P<second>\d{2}))?
            )?
            \b
            """,
            re.VERBOSE,
        )
        pattern2 = re.compile(
            r"""
            \b
            (?P<hour>\d{1,2}):(?P<minute>\d{2})
            (?::(?P<second>\d{2}))?
            \s+
            (?P<day>\d{1,2})/(?P<month>\d{1,2})/(?P<year>\d{2,4})
            \b
            """,
            re.VERBOSE,
        )

        for pattern in (pattern1, pattern2):
            if match := pattern.search(text):
                gd = match.groupdict()
                day = int(gd["day"])
                month = int(gd["month"])
                year = int(gd["year"])
                if year < 100:
                    year += 2000
                hour = int(gd.get("hour") or 0)
                minute = int(gd.get("minute") or 0)
                second = int(gd.get("second") or 0)
                try:
                    return datetime(year, month, day, hour, minute, second)
                except ValueError:
                    return None
        return None

    @staticmethod
    def _parse_dot_date(text: str) -> datetime | None:
        """
        Parse date strings in the format 'DD.MM.YYYY' or 'DD.MM.YYYY HH:MM[:SS]'.
        Returns a datetime object or None.
        """
        pattern = re.compile(
            r"""
            \b
            (?P<day>\d{1,2})\.(?P<month>\d{1,2})\.(?P<year>\d{4})
            (?:\s+
                (?P<hour>\d{1,2}):(?P<minute>\d{2})
                (?::(?P<second>\d{2}))?
            )?
            \b
            """,
            re.VERBOSE,
        )
        if match := pattern.search(text):
            gd = match.groupdict()
            day = int(gd["day"])
            month = int(gd["month"])
            year = int(gd["year"])
            hour = int(gd.get("hour") or 0)
            minute = int(gd.get("minute") or 0)
            second = int(gd.get("second") or 0)
            try:
                return datetime(year, month, day, hour, minute, second)
            except ValueError:
                return None
        return None

    @staticmethod
    def _parse_time_only(text: str) -> datetime | None:
        """
        Parse time-only strings like '23:00' or '23:00:00'.
        If the time has already passed today, return the same time for tomorrow.
        Returns a datetime object.
        """
        pattern = re.compile(r"\b(?P<hour>\d{1,2}):(?P<minute>\d{2})(?::(?P<second>\d{2}))?\b")
        match = pattern.search(text)
        if not match:
            return None

        now = datetime.now()
        gd = match.groupdict(default="0")
        hour = int(gd["hour"])
        minute = int(gd["minute"])
        second = int(gd["second"]) if gd.get("second") else 0

        try:
            candidate = datetime(now.year, now.month, now.day, hour, minute, second)
        except ValueError:
            return None

        if candidate <= now:
            candidate += timedelta(days=1)
        return candidate

    @staticmethod
    def _parse_iso8601(text: str) -> datetime | None:
        """
        Parse ISO-8601 formatted strings like '2025-06-01T12:30:00'.
        Returns a datetime object.
        """
        pattern = re.compile(
            r"\b(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})[T\s]"
            r"(?P<hour>\d{2}):(?P<minute>\d{2}):(?P<second>\d{2})\b"
        )
        match = pattern.search(text)
        if not match:
            return None
        gd = match.groupdict()
        try:
            return datetime(
                int(gd["year"]), int(gd["month"]), int(gd["day"]), int(gd["hour"]), int(gd["minute"]), int(gd["second"])
            )
        except ValueError:
            return None

    @staticmethod
    def _parse_unix_timestamp(text: str) -> datetime | None:
        """
        Parse Unix timestamps (10 or 13 digit integers).
        Supports timestamps in seconds or milliseconds.
        Returns a datetime object.
        """
        match = re.search(r"\b\d{10,13}\b", text)
        if not match:
            return None

        timestamp = match.group()
        try:
            ts_int = int(timestamp)
            if len(timestamp) == 13:
                ts_int //= 1000  # convert from ms to seconds
            return datetime.fromtimestamp(ts_int)
        except (ValueError, OSError):
            return None

    def parse_time_text(self, content: str) -> datetime | timedelta | None:
        """
        Orchestrate parsing attempts using various supported time formats.
        Returns a datetime or timedelta if a format is successfully parsed, otherwise None.
        Supported formats include:
        - duration strings (e.g., '2h 30m')
        - dd/mm/yyyy or dd/mm/yyyy hh:mm
        - dd.mm.yyyy or dd.mm.yyyy hh:mm
        - HH:MM (today or tomorrow)
        - ISO-8601 (e.g., 2025-06-01T12:30:00)
        - Unix timestamps (seconds or milliseconds)
        """
        content = content.strip()

        for parser in [
            self._parse_duration,
            self._parse_datetime_with_date,
            self._parse_dot_date,
            self._parse_iso8601,
            self._parse_unix_timestamp,
            self._parse_time_only,
        ]:
            if result := parser(content):
                return result
        return None

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
