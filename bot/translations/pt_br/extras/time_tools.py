# -*- coding: utf-8 -*-
from __future__ import annotations, annotations, annotations

import re
from datetime import datetime, timedelta, timezone
from typing import Optional, Union

import humanize

humanize.activate("pt_BR")


class TimeTools:
    def __init__(self):
        pass

    YEAR = "ano"
    DAY = "dia"
    HOUR = "hora"
    MINUTE = "minuto"
    SECOND = "segundo"
    YY = "a"
    DD = "d"
    HH = "h"
    MM = "min"
    SS = "s"

    # pattern_relative_time = re.compile(
    #     r"""
    #     (?:in|daqui)\s
    #     (\b(?P<years>\d+)\s?(?:anos|ano|a)\b\s?)?
    #     (\b(?P<months>\d+)\s?(?:meses|mês|mes)\b\s?)?
    #     (\b(?P<weeks>\d+)\s?(?:semanas|semana)\b\s?)?
    #     (\b(?P<days>\d+)\s?(?:dias|dia|d)\b\s?)?
    #     (\b(?P<hours>\d+)\s?(?:horas|hora|h)\b\s?)?
    #     (\b(?P<minutes>\d+)\s?(?:minutos|minuto|min|m)\b\s?)?
    #     (\b(?P<seconds>\d+)\s?(?:segundos|segundo|seg|s)\b\s?)?
    #     """,
    #     re.VERBOSE,
    # )

    pattern_relative_time = re.compile(r"""
        (\b(?P<years>\d+)\s?(?:anos|ano|a|years|year|y)\b\s?)?
        (\b(?P<months>\d+)\s?(?:meses|mês|mes|months|month|mo)\b\s?)?
        (\b(?P<weeks>\d+)\s?(?:semanas|semana|weeks|week|w)\b\s?)?
        (\b(?P<days>\d+)\s?(?:dias|dia|d|days|day)\b\s?)?
        (\b(?P<hours>\d+)\s?(?:horas|hora|h|hours|hour)\b\s?)?
        (\b(?P<minutes>\d+)\s?(?:minutos|minuto|min|m|minutes|minute)\b\s?)?
        (\b(?P<seconds>\d+)\s?(?:segundos|segundo|seg|s|seconds|second|secs|sec)\b\s?)?
        """, re.VERBOSE, )

    pattern_absolute_time_and_date = re.compile(r"""
        (?:on|em)\s
        (?:\b
            (?P<hour>[01]?[0-9]|2[0-3])
            [h:]
            (?P<minute>[0-5][0-9])?
            :?
            (?P<second>[0-5][0-9])?
        \b\s?)?
        (?:\b
            (?P<day>0?[1-9]|[12][0-9]|3[01])
            [\/-]
            (?P<month>0?[1-9]|1[012])
            (?:[\/-](?P<year>[0-9]{4}))?
        \b\s?)?
        """, re.VERBOSE, )

    def birthday(self, target: str) -> Optional[str]:
        if "ano" in target and not any(x in target for x in ["mês", "meses", "semana", "dia"]):
            return " ".join(target.split()[:2])

    def clean(self, target: Union[datetime, timedelta]) -> Union[datetime, str]:
        if isinstance(target, timedelta):
            return str(target).split(".")[0]
        if isinstance(target, datetime):
            # return target.replace(microsecond=0)
            return target.replace(tzinfo=timezone.utc).replace(microsecond=0)

    def date_in_full(self, delta: timedelta) -> str:
        y, d = divmod(delta.days, 365)
        M, d = divmod(d, 30)
        m, s = divmod(delta.seconds, 60)
        H, m = divmod(m, 60)
        response = ""
        for value, unit in zip([y, M, d], ["ano", "mês", "dia"]):
            if value:
                unit = unit if value == 1 else "meses" if unit == "mês" else unit + "s"
                response += f"{value} {unit} "
        response += f"{H:02d}:{m:02d}:{s:02d}"
        return response.rstrip(", ")

    def find_relative_time(self, target: str) -> Optional[re.Match]:
        match = self.pattern_relative_time.match(target)
        if match and any(match.groups()[1:]):
            return match

    def find_absolute_time(self, target: str) -> Optional[re.Match]:
        match = self.pattern_absolute_time_and_date.match(target)
        if match and any(match.groups()[1:]):
            return match

    def format(self, target: datetime) -> str:
        return (target - timedelta(hours=3)).strftime("%d/%m/%y às %H:%M:%S")

    def on_cooldown(self, target: datetime, now: datetime = None, s: int = 0) -> Optional[timedelta]:
        now = now or datetime.now()
        delta = self.clean(now) - self.clean(target)
        a = delta.total_seconds()
        if delta.total_seconds() <= s:
            return timedelta(seconds=s) - delta

    def timeago(self, target: datetime, now: datetime = None, full: bool = True) -> Union[str, timedelta]:
        now = now or datetime.now()
        delta = self.clean(now) - self.clean(target)
        if full:
            return self.date_in_full(delta)
        return delta


class Humanize:
    # TODO: Fazer com que a linguagem to humanize varie de acordo com a língua do usuário.

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


class Timeago:
    def __init__(self, target: datetime, *, now: datetime = None, reverse: bool = False) -> None:
        if now is None:
            now = datetime.utcnow()
        target = target.replace(tzinfo=None)
        now = now.replace(tzinfo=None)
        if reverse:
            target, now = now, target
        if target > now:
            raise ValueError()
        self.delta = now - target
        yy, dd = divmod(self.delta.days, 365)
        mm, ss = divmod(self.delta.seconds, 60)
        hh, mm = divmod(mm, 60)
        self.years = yy
        self.days = dd
        self.hours = hh
        self.minutes = mm
        self.seconds = ss

    def total_in_seconds(self) -> float:
        return self.delta.total_seconds()

    def humanize(self, *, precision: int = 2, minimum: str = "s", short: bool = False) -> str:
        quote = ""
        for value, name, symbol in [(self.years, TimeTools.YEAR, TimeTools.YY),
                (self.days, TimeTools.DAY, TimeTools.DD), (self.hours, TimeTools.HOUR, TimeTools.HH),
                (self.minutes, TimeTools.MINUTE, TimeTools.MM), (self.seconds, TimeTools.SECOND, TimeTools.SS), ]:
            if value <= 0:
                continue
            if symbol > minimum:
                continue
            if len(quote.split()) >= precision * (int(not short) + 1):
                break
            unit = symbol if short else f" {name}"
            plural = "s" if value != 1 and not short else ""
            quote += f" {value}{unit}{plural}"
        quote = quote.strip()
        if quote:
            return " ".join(quote.split()[: 2 * precision])
        return "pouco tempo"
