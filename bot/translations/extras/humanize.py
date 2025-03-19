from datetime import datetime, UTC
import humanize
from .response import BaseFunctions


class HumanizeContext:
    def __init__(self, lang):
        self.lang = lang

    def __enter__(self):
        if self.lang != 'en':
            humanize.activate(self.lang)

    def __exit__(self, exc_type, exc_val, exc_tb):
        humanize.deactivate()


class Humanize:
    _years = ["months", "days", "hours", "minutes", "seconds", "milliseconds", "microseconds"]
    _months = ["years", "days", "hours", "minutes", "seconds", "milliseconds", "microseconds"]
    _weeks = ["years", "months", "hours", "minutes", "seconds", "milliseconds", "microseconds"]
    _days = ["years", "months", "hours", "minutes", "seconds", "milliseconds", "microseconds"]
    _hours = ["years", "months", "days", "minutes", "seconds", "milliseconds", "microseconds"]
    _minutes = ["years", "months", "days", "hours", "seconds", "milliseconds", "microseconds"]
    _seconds = ["years", "months", "days", "hours", "minutes", "milliseconds", "microseconds"]
    _microseconds = ["years", "months", "days", "hours", "minutes", "seconds", "milliseconds"]
    _milliseconds = ["years", "months", "days", "hours", "minutes", "seconds", "microseconds"]

    def __init__(self, data: dict, pattern_time: dict):
        self.lang = data["language"] or "en"
        self.units = self._generate_options(pattern_time)

    def precisedelta(self, value, minimum_unit="seconds", suppress=(), format="%0.2f") -> str:
        with HumanizeContext(self.lang):
            response = humanize.precisedelta(value, minimum_unit=minimum_unit, suppress=suppress, format=format)
        return response

    def naturaltime(self, value, future: bool = False, months: bool = True, minimum_unit: str = "seconds",
                    when: datetime = None, ) -> str:
        with HumanizeContext(self.lang):
            response = humanize.naturaltime(value, future=future, months=months, minimum_unit=minimum_unit, when=when)
        return response

    def naturaldelta(self, value, months: bool = True, minimum_unit: str = "seconds") -> str:
        with HumanizeContext(self.lang):
            response = humanize.naturaldelta(value, months=months, minimum_unit=minimum_unit)
        return response

    def naturaldate(self, value) -> str:
        with HumanizeContext(self.lang):
            response = humanize.naturaldate(value)
        return response

    def naturalsize(self, value, binary: bool = False, gnu: bool = False, format: str = "%.1f") -> str:
        with HumanizeContext(self.lang):
            response = humanize.naturalsize(value, binary=binary, gnu=gnu, format=format)
        return response

    def _generate_options(self, units: dict):
        options = {}  # NOQA
        for value in units["years"]:
            options[value] = self._years
        for value in units["months"]:
            options[value] = self._months
        for value in units["weeks"]:
            options[value] = self._weeks
        for value in units["days"]:
            options[value] = self._days
        for value in units["hours"]:
            options[value] = self._hours
        for value in units["minutes"]:
            options[value] = self._minutes
        for value in units["seconds"]:
            options[value] = self._seconds
        for value in units["milliseconds"]:
            options[value] = self._milliseconds
        for value in units["microseconds"]:
            options[value] = self._microseconds
        options["time"] = ()
        return options

    def created_a_time(self, created_at: datetime, timezone=UTC):
        return humanize.precisedelta(datetime.now(timezone) - created_at.astimezone(timezone))

    def updated_a_time(self, updated_at: datetime, timezone=UTC):
        return humanize.precisedelta(datetime.now(timezone) - updated_at.astimezone(timezone))










