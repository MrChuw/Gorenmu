from datetime import datetime

import humanize

humanize.activate("pt_BR")


class Humanize:
    @staticmethod
    def precisedelta(value, minimum_unit="seconds", suppress=(), format="%0.2f") -> str:
        return humanize.precisedelta(value, minimum_unit=minimum_unit, suppress=suppress, format=format)

    @staticmethod
    def naturaltime(value, future: bool = False, months: bool = True, minimum_unit: str = "seconds",
                    when: datetime = None, ) -> str:
        return humanize.naturaltime(value, future=future, months=months, minimum_unit=minimum_unit, when=when)

    @staticmethod
    def naturaldelta(value, months: bool = True, minimum_unit: str = "seconds") -> str:
        return humanize.naturaldelta(value, months=months, minimum_unit=minimum_unit)

    @staticmethod
    def naturaldate(value) -> str:
        return humanize.naturaldate(value)

    @staticmethod
    def naturalsize(value, binary: bool = False, gnu: bool = False, format: str = "%.1f") -> str:
        return humanize.naturalsize(value, binary=binary, gnu=gnu, format=format)
