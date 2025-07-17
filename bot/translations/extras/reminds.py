# -*- coding: utf-8 -*-
import re


class RemindTime:
    def __init__(self, time_units: dict) -> None:
        self.PATTERN_TIME = self.generate_time_regex(time_units)

    @staticmethod
    def generate_time_regex(time_units: dict) -> re.Pattern:
        patterns = []
        patterns.extend(rf"(\b(?P<{unit}>\d+)\s?(?:{'|'.join(terms)})\b\s?)?" for unit, terms in time_units.items())
        return re.compile(r"\n".join(patterns), re.VERBOSE)
