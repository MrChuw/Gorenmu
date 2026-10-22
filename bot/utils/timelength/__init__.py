"""
A flexible python duration parser designed for human-readable lengths of time.
https://github.com/EtorixDev/timelength/blob/main/LICENSE
"""

from bot.utils.timelength.dataclasses import Numeral, ParsedTimeLength, ParserSettings, Scale
from bot.utils.timelength.enums import FailureFlags
from bot.utils.timelength.errors import (
    InvalidLocaleError,
    InvalidNumeralError,
    InvalidParserError,
    InvalidScaleError,
    NotALocaleError,
    NoValidScalesError,
    ParsedTimeDeltaError,
    PotentialDateTimeError,
    PotentialTimeDeltaError,
)
from bot.utils.timelength.locales import English, Guess, Locale, Portuguese, Spanish
from bot.utils.timelength.parsers.date_parser import DateParserConfig, preprocess_dates
from bot.utils.timelength.timelength import TimeLength

__all__ = [
    "DateParserConfig",
    "English",
    "FailureFlags",
    "Guess",
    "InvalidLocaleError",
    "InvalidNumeralError",
    "InvalidParserError",
    "InvalidScaleError",
    "Locale",
    "NoValidScalesError",
    "NotALocaleError",
    "Numeral",
    "ParsedTimeDeltaError",
    "ParsedTimeLength",
    "ParserSettings",
    "Portuguese",
    "PotentialDateTimeError",
    "PotentialTimeDeltaError",
    "Scale",
    "Spanish",
    "TimeLength",
    "preprocess_dates",
]
