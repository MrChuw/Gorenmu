from datetime import datetime
import humanize


class HumanizeContext:
    def __init__(self, lang):
        self.lang = lang

    def __enter__(self):
        if self.lang != 'en':
            humanize.activate(self.lang)

    def __exit__(self, exc_type, exc_val, exc_tb):
        humanize.deactivate()


class Humanize:
    def __init__(self, data: tuple):
        self.lang = data[0]["language"] if data[0]["language"] is not None else data[1]["language"]

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
