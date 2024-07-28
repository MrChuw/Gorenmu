# -*- coding: utf-8 -*-
from __future__ import annotations

import re

PATTERN_TIME = re.compile(
    r"""
    (\b(?P<years>\d+)\s?(?:anos|ano|a|years|year|y)\b\s?)?
    (\b(?P<months>\d+)\s?(?:meses|mês|mes|months|month|mo)\b\s?)?
    (\b(?P<weeks>\d+)\s?(?:semanas|semana|weeks|week|w)\b\s?)?
    (\b(?P<days>\d+)\s?(?:dias|dia|d|days|day)\b\s?)?
    (\b(?P<hours>\d+)\s?(?:horas|hora|h|hours|hour)\b\s?)?
    (\b(?P<minutes>\d+)\s?(?:minutos|minuto|min|m|minutes|minute)\b\s?)?
    (\b(?P<seconds>\d+)\s?(?:segundos|segundo|seg|s|seconds|second|secs|sec)\b\s?)?
    """,
    re.VERBOSE,
)
