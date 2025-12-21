from __future__ import annotations

import unicodedata
from datetime import datetime
from typing import TYPE_CHECKING

from bot.utils.timelength.enums import CharacterType, ValueType

if TYPE_CHECKING:
    from bot.utils.timelength.locales import Locale


def is_int(num: str | int | float) -> bool:
    """Check if the passed string is an integer."""
    try:
        num_int = int(float(num))
        return num_int == float(num)
    except ValueError:
        return False


def is_number(num: str) -> bool:
    """Check if the passed string is a number."""
    try:
        float(num)
        return True
    except ValueError:
        return False


def character_type(text: str) -> CharacterType:
    """Check the type of character based on the `CharacterType` enum."""
    if is_number(text):
        return CharacterType.NUMBER
    elif text.isalpha():
        return CharacterType.ALPHABET
    else:
        return CharacterType.SYMBOL


def value_type(text: str, scale_terms: list, numeral_terms: list, symbol_terms: list) -> ValueType:
    """Check the type of string based on the `ValueType` enum."""
    if isinstance(text, datetime):
        return ValueType.DATE
    elif is_number(text):
        return ValueType.NUMBER
    elif text in scale_terms:
        return ValueType.SCALE
    elif text in numeral_terms:
        return ValueType.NUMERAL
    elif text in symbol_terms:
        return ValueType.SYMBOL
    else:
        return ValueType.MIXED


def remove_diacritics(text: str) -> str:
    """Replace accented and special characters with their normalized equivalents."""
    nfkd_form = unicodedata.normalize("NFKD", text)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])


class DetectNumberSegmentHelper:
    def __init__(self, locale: Locale):
        self.locale = locale

    def is_number_segment_char(self, char: str) -> bool:
        return character_type(char) is CharacterType.NUMBER or char in self.locale.connectors + self.locale.delimiters

    @staticmethod
    def update_hhmmss_date_state(current_char: str, encountered: bool, hhmmss_date_delimiters: set[str]) -> bool:
        return encountered or current_char in hhmmss_date_delimiters

    def update_trailing_connectors(self, current_char: str, trailing: int) -> int:
        return trailing + 1 if current_char in self.locale.connectors else 0

    def is_invalid_connector_or_segmenter(
        self, current_char: str, prev_char: str | None, next_char: str | None
    ) -> bool:
        if current_char in self.locale.segmenters:
            return True

        if current_char in self.locale.connectors:
            return (
                prev_char not in self.locale.connectors + self.locale.delimiters
                or next_char not in self.locale.connectors + self.locale.delimiters
            )

        return False

    def should_break_decimal(self, current_char: str, next_char: str | None, content: str, index: int) -> bool:
        if current_char not in self.locale.decimal_delimiters or not next_char:
            return False

        if character_type(next_char) is CharacterType.NUMBER:
            return False

        temp_index = index + 1
        while temp_index < len(content):
            char_type = character_type(content[temp_index])
            if char_type is not CharacterType.SYMBOL:
                return char_type is not CharacterType.NUMBER
            temp_index += 1

        return True

    def should_break_thousand_delimiter(
        self,
        *,
        current_char: str,
        prev_char: str | None,
        next_char: str | None,
        encountered_hhmmss_or_date: bool,
        min_thousand_digits: int,
        content: str,
        index: int,
        hhmmss_date_delimiters: set[str],
    ) -> bool:
        if current_char not in self.locale.thousand_delimiters:
            return False

        if prev_char in hhmmss_date_delimiters or next_char in hhmmss_date_delimiters:
            return False

        prev_type = character_type(prev_char) if prev_char else None
        next_type = character_type(next_char) if next_char else None

        return (
            (next_char in self.locale.connectors and next_char != current_char)
            or (next_char in self.locale.thousand_delimiters and next_char not in self.locale.connectors)
            or (
                current_char in self.locale.connectors
                and prev_type is CharacterType.NUMBER
                and next_type is CharacterType.NUMBER
                and not all(
                    (index + i) < len(content) and character_type(content[index + i]) is CharacterType.NUMBER
                    for i in range(1, min_thousand_digits + 1)
                )
            )
            or (
                prev_type is CharacterType.NUMBER
                and next_type is not CharacterType.NUMBER
                and next_char not in self.locale.connectors + self.locale.delimiters
            )
            or (
                next_type is CharacterType.NUMBER
                and prev_type is not CharacterType.NUMBER
                and not encountered_hhmmss_or_date
            )
        )

    def should_break_isolated_connector(
        self,
        current_char: str,
        prev_char: str | None,
        next_char: str | None,
        encountered_hhmmss_or_date: bool,
        hhmmss_date_delimiters: set[str],
    ) -> bool:
        return (
            current_char in self.locale.connectors
            and current_char not in hhmmss_date_delimiters
            and prev_char not in hhmmss_date_delimiters
            and next_char not in hhmmss_date_delimiters
            and character_type(next_char) is CharacterType.NUMBER
            and not encountered_hhmmss_or_date
        )
