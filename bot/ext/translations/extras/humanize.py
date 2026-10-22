import re
from contextvars import ContextVar
from datetime import UTC, date, datetime, timedelta, tzinfo

import humanize

_current_tz: ContextVar[tzinfo | None] = ContextVar("current_tz", default=None)


class HumanizeContext:
    def __init__(self, lang: str = "en", tz: tzinfo | None = None):
        self.lang = lang
        self.tz = tz
        self._token = None

    def __enter__(self):
        if self.lang != "en":
            humanize.activate(self.lang)
        if self.tz is not None:
            self._token = _current_tz.set(self.tz)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        humanize.deactivate()
        if self._token is not None:
            _current_tz.reset(self._token)


class Humanize:
    def __init__(self, pattern_time: dict, lang: str, fallback_pattern: dict | None = None):
        self.lang = lang
        self.units: dict[str, list[str]]
        pattern = pattern_time
        if fallback_pattern:
            pattern = pattern_time | fallback_pattern
        self._generate_options(pattern)
        self.pattern = pattern

    @staticmethod
    def set_tz(tz: tzinfo | None):
        resolved_tz = tz
        _current_tz.set(resolved_tz)

    @property
    def current_tz(self) -> tzinfo | None:
        return _current_tz.get()

    def _get_now(self) -> datetime:
        tz = self.current_tz
        return datetime.now(tz) if tz else datetime.now()

    def _to_user_tz(self, dt: datetime) -> datetime:
        """Converte ou atribui o timezone do usuário ao datetime."""
        if tz := self.current_tz:
            return dt.replace(tzinfo=tz) if dt.tzinfo is None else dt.astimezone(tz)
        else:
            return dt

    def _as_timedelta(self, value: datetime | timedelta | int | float) -> timedelta | int | float:
        """
        Converte datetime para timedelta relativo ao fuso configurado.
        Evita que o humanize chame datetime.now() naive internamente.
        """
        if isinstance(value, datetime):
            target = self._to_user_tz(value)
            return self._get_now() - target
        return value

    def precisedelta(
        self,
        value: datetime | timedelta | int | float,
        minimum_unit: str = "seconds",
        suppress: tuple[str, ...] = (),
        format: str = "%0.2f",
    ) -> str:
        delta = self._as_timedelta(value)
        with HumanizeContext(self.lang):
            return humanize.precisedelta(
                int(delta) if isinstance(delta, float) else delta,
                minimum_unit=minimum_unit,
                suppress=suppress or (),
                format=format,
            )

    def naturaltime(
        self,
        value: datetime | timedelta,
        future: bool = False,
        months: bool = True,
        minimum_unit: str = "seconds",
        when: datetime | None = None,
    ) -> str:
        with HumanizeContext(self.lang):
            target = value
            ref_when = when or self._get_now()

            if isinstance(target, datetime):
                target = self._to_user_tz(target)

            return humanize.naturaltime(
                target,
                future=future,
                months=months,
                minimum_unit=minimum_unit,
                when=ref_when,
            )

    def naturaldelta(self, value: timedelta, months: bool = True, minimum_unit: str = "seconds") -> str:
        delta = self._as_timedelta(value)
        with HumanizeContext(self.lang):
            return humanize.naturaldelta(delta, months=months, minimum_unit=minimum_unit)

    def naturaldate(self, value: date | datetime) -> str:
        with HumanizeContext(self.lang):
            if isinstance(value, datetime):
                target_date = self._to_user_tz(value).date()
            elif isinstance(value, date):
                target_date = value

            delta_days = (target_date - self._get_now().date()).days
            if delta_days == 0:
                return humanize.naturaldate(date.today())
            if delta_days == 1:
                return humanize.naturaldate(date.today() + timedelta(days=1))
            if delta_days == -1:
                return humanize.naturaldate(date.today() - timedelta(days=1))

            return target_date.strftime("%d/%m/%Y")

    def naturalsize(
        self, value: int | float | str, binary: bool = False, gnu: bool = False, format: str = "%.1f"
    ) -> str:
        with HumanizeContext(self.lang):
            return humanize.naturalsize(value, binary=binary, gnu=gnu, format=format)

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

    def generate_time_regex(self, exclude: list[str] | None = None) -> re.Pattern:
        if exclude is None:
            exclude = ["time", "t"]
        patterns = [
            rf"(\b(?P<{unit}>\d+)\s?(?:{'|'.join(self.pattern[unit])})\b\s?)?"
            for unit in self.pattern
            if unit not in exclude
        ]
        return re.compile(r"\s*".join(patterns), re.VERBOSE)

    def created_a_time(self, created_at: datetime, timezone=UTC):
        with HumanizeContext(self.lang):
            return humanize.precisedelta(datetime.now(timezone) - created_at.astimezone(timezone))

    def updated_a_time(self, updated_at: datetime, timezone=UTC):
        with HumanizeContext(self.lang):
            return humanize.precisedelta(datetime.now(timezone) - updated_at.astimezone(timezone))
