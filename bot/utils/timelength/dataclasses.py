from __future__ import annotations

import json
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Literal

from bot.utils.timelength.enums import FailureFlags, NumeralType
from bot.utils.timelength.parsers.common import remove_diacritics


def _expand_terms(terms: Sequence[str]) -> tuple[str, ...]:
    """Expand a list of terms into lower/title/upper case variants, with diacritics stripped."""
    expanded: tuple[str, ...] = ()
    for term in terms:
        term = remove_diacritics(term)
        if len(term) == 1:
            expanded += (term.lower(), term.upper())
        else:
            expanded += (term.lower(), term.title(), term.upper())
    return expanded


class Scale:
    """---
    Represents a timescale.

    #### Attributes
    - key: `str` — The internal identifier of the scale (ex: "minute").
    - scale: `float = 0.0` — The number of seconds in the scale.
    - singular: `str = ""` — The singular form of the scale.
    - plural: `str = ""` — The plural form of the scale.
    - terms: `tuple[str, ...] = ()` — A tuple of terms associated with the scale.
    - enabled: `bool = True` — Whether the scale is enabled or not.

    #### Properties
    - valid: `bool` — Return whether the scale is valid or not based on all attributes being set.
    """

    def __init__(self, key: str, scale: float, singular: str, plural: str, terms: Sequence[str]) -> None:
        self.key: str = key
        self.scale: float = scale
        self.singular: str = singular
        self.plural: str = plural
        self.terms: tuple[str, ...] = _expand_terms(terms)
        self.enabled: bool = True

    @property
    def valid(self) -> bool:
        """Return whether the scale is valid or not based on all attributes being set."""
        return bool(self.scale and self.singular and self.plural and self.terms)

    def __str__(self) -> str:
        """Return the title cased singular form of the scale."""
        return self.singular.title()

    def __repr__(self) -> str:
        """Return a string representation of the scale with attributes included."""

        def tuple_to_str(tup: tuple[str, ...]) -> str:
            return "(" + ", ".join([json.dumps(term) for term in tup]) + ")"

        terms_str = tuple_to_str(self.terms)
        return (
            f"Scale(scale={self.scale}, key={self.key}, singular={json.dumps(self.singular)}, "
            f"plural={json.dumps(self.plural)}, terms={terms_str}, enabled={self.enabled})"
        )

    def __eq__(self, value: object) -> bool:
        """Return whether the scale is equal to the value."""
        return self.scale == value.scale if isinstance(value, Scale) else False

    def __hash__(self) -> int:
        """Return the hash of the scale."""
        return hash((self.key, self.scale, self.singular, self.plural, self.terms, self.enabled))


class Numeral:
    """---
    Represents a number related word.

    #### Attributes
    - name: `str = ""` — The name of the numeral.
    - type: `NumeralType = NumeralType.NONE` — The type of numeral.
    - value: `float = 0.0` — The value of the numeral.
    - terms: `tuple[str, ...] = ()` — A tuple of terms associated with the numeral.

    #### Properties
    - valid: `bool` — Return whether the numeral is valid or not based on all attributes being set.
    """

    def __init__(self, name: str, type: NumeralType, value: float, terms: Sequence[str]) -> None:
        self.name: str = name
        self.type: NumeralType = type
        self.value: float = value
        self.terms: tuple[str, ...] = _expand_terms(terms)
        self.enabled: bool = True

    @property
    def valid(self) -> bool:
        """Return whether the numeral is valid or not based on all attributes being set."""
        return bool(
            self.name and self.type and self.type is not NumeralType.NONE and self.value is not None and self.terms
        )

    def __str__(self) -> str:
        """Return the title cased singular form of the numeral."""
        return self.name.title()

    def __repr__(self) -> str:
        """Return a string representation of the numeral with attributes included."""

        def tuple_to_str(tup: tuple[str, ...]) -> str:
            return "(" + ", ".join([json.dumps(term) for term in tup]) + ")"

        terms_str = tuple_to_str(self.terms)
        return (
            f"Numeral(name={json.dumps(self.name)}, type={self.type}, "
            f"value={self.value}, terms={terms_str}, enabled={self.enabled})"
        )

    def __eq__(self, value: object) -> bool:
        """Return whether the numeral is equal to the value."""
        return self.value == value.value if isinstance(value, Numeral) else False

    def __hash__(self) -> int:
        """Return the hash of the numeral."""
        return hash((self.name, self.type, self.value, self.terms, self.enabled))


class ParsedTimeLength:
    """
    Represents the outcome of parsing a TimeLength.

    #### Properties
    - success: `bool` — Indicates if the parsing was successful.
    - seconds: `float` — The total length of time parsed, in seconds.
    - delta: `timedelta | None` — The parsed time as a `timedelta`, or `None` if out of range.
    - invalid: `tuple` — The parts of the input string that could not be parsed as valid time.
    - valid: `tuple` — The parts of the input string that were successfully parsed as valid time.
    - found_date: `bool` — Whether a date was found within the input.
    - date: `datetime | None` — The date found within the input, if any.
    - remaining_text: `str` — `content` with every span that contributed to `valid` or `date`
        stripped out. Spans that ended up in `invalid` are intentionally left untouched, since they
        may still be meaningful words the parser simply didn't recognize.
    - matched_text: `str` — The exact complement of `remaining_text`: just the span(s) that
        contributed to `valid` or `date`, concatenated in their original order.
    """

    def __init__(
        self,
        success: bool = False,
        seconds: float = 0.0,
        delta: timedelta | None = None,
        invalid: tuple[tuple[float | str, FailureFlags], ...] = (),
        valid: tuple[tuple[float, Scale], ...] = (),
        found_date: bool = False,
        date: datetime | None = None,
        remaining_text: str = "",
        matched_text: str = "",
    ) -> None:
        self._success: bool = success
        self._seconds: float = seconds
        self._delta: timedelta | None = delta
        self._invalid: tuple[tuple[float | str, FailureFlags], ...] = invalid
        self._valid: tuple[tuple[float, Scale], ...] = valid
        self.found_date: bool = found_date
        self.date: datetime | None = date
        self._remaining_text: str = remaining_text
        self._matched_text: str = matched_text

    @property
    def success(self) -> bool:
        """Return if the parsing was successful."""
        return self._success

    @property
    def seconds(self) -> float:
        """Return the total length of time parsed, in seconds."""
        return self._seconds

    @property
    def delta(self) -> timedelta | None:
        """Return a timedelta representing the parsed time, or None if out of range."""
        return self._delta

    @property
    def invalid(self) -> tuple[tuple[float | str, FailureFlags], ...]:
        """Return a tuple of parts of the input string that could not be parsed as valid time."""
        return self._invalid

    @property
    def valid(self) -> tuple[tuple[float, Scale], ...]:
        """Return a tuple of parts of the input string that were successfully parsed as valid time."""
        return self._valid

    @property
    def remaining_text(self) -> str:
        """---
        Return `content` with every span that contributed to `valid` or `date` stripped out.

        Useful to separate a recognized time expression from the rest of a free-form message.

        #### Example
        ```python
        tl = TimeLength("as 19:22:22 do dia 12/02/2029 sobre o blablabla", locale=Portuguese())
        print(tl.result.remaining_text)  # "sobre o blablabla" (plus any invalid leftover words)
        ```
        """
        return self._remaining_text

    @property
    def matched_text(self) -> str:
        """The exact complement of `remaining_text` — just the recognized date/duration span(s)."""
        return self._matched_text

    def __str__(self) -> str:
        """Return a string indicating the success or failure of the parsing."""
        return "Success" if self.success else "Failure"

    def __repr__(self) -> str:
        """Return a string representation of the ParsedTimeLength with attributes included."""

        def tuple_to_str(tup: tuple) -> str:
            return (
                "("
                + ", ".join(
                    [
                        (
                            tuple_to_str(term)
                            if isinstance(term, tuple)
                            else repr(term)
                            if isinstance(term, (Scale, FailureFlags))
                            else json.dumps(term)
                        )
                        for term in tup
                    ]
                )
                + ")"
            )

        valid_str = tuple_to_str(self.valid)
        invalid_str = tuple_to_str(self.invalid)
        return (
            f"ParsedTimeLength(success={self.success}, seconds={self.seconds}, "
            f"invalid={invalid_str}, valid={valid_str}, found_date={self.found_date}, "
            f"remaining_text={json.dumps(self.remaining_text)})"
        )


@dataclass()
class Buffer:
    """---
    Represents the state of the buffer during parsing.

    #### Attributes
    - value: `str | float | datetime = ""` — The current value of the buffer.
        - While usually a `str` being built character by character, it may temporarily hold an
            already-resolved `float` (parsed number) or `datetime` (parsed date) pending flush.
    """

    value: str | float | datetime = ""

    def __str__(self) -> str:
        """Return the current value of the buffer."""
        return str(self.value)

    def __repr__(self) -> str:
        """Return a string representation of the buffer with attributes included."""
        return f"Buffer(value={json.dumps(self.value) if isinstance(self.value, str) else self.value!r})"


@dataclass()
class ParserSettings:
    """---
    Represents the settings for the parser.

    #### Attributes
    - assume_scale: `Literal["LAST", "SINGLE", "NEVER"] = "SINGLE"` — How to handle no scale being provided.
        - `LAST` will assume seconds only for the last value if no scale is provided for it.
        - `SINGLE` will only assume seconds when a single input is provided.
        - `NEVER` will never assume seconds when no scale is provided.
    - limit_allowed_terms: `bool = True` — Prevent terms from the `allowed_terms` list in
        the config from being used in the middle of a segment, thus interrupting a value/scale pair.
        - The affected segment will become abandoned and added to the invalid list.
        - The terms may still be used at the beginning or end of a segment/sentence.
        - If `False`, The terms will be ignored (within other limitations) and not affect parsing.
    - allow_duplicate_scales: `bool = True` — Allow scales to be parsed multiple times, stacking their values.
        - If `False`, the first scale will be used and subsequent duplicates will be added to the invalid list.
    - allow_thousands_extra_digits: `bool = False` — Allow thousands to be parsed with more than three digits
        following the thousand delimiter.
        - Ex: `1,2345` will be interpreted as `12,345`.
    - allow_thousands_lacking_digits: `bool = False` — Allow thousands to be parsed with less than three digits.
        - Ex: `1,23` will be interpreted as `123`.
    - allow_decimals_lacking_digits: `bool = True` — Allow decimals to be parsed with no number following the
        decimal delimiter.
        - Ex: `1.` will be interpreted as `1.0`.
    """

    assume_scale: Literal["LAST", "SINGLE", "NEVER"] = "SINGLE"
    limit_allowed_terms: bool = True
    allow_duplicate_scales: bool = True
    allow_thousands_extra_digits: bool = False
    allow_thousands_lacking_digits: bool = False
    allow_decimals_lacking_digits: bool = True

    def __str__(self) -> str:
        """Return the settings as either 'Default' or 'Modified' based on the default values."""
        return (
            "Modified"
            if any(
                [
                    self.assume_scale != "SINGLE",
                    self.limit_allowed_terms is False,
                    self.allow_duplicate_scales is False,
                    self.allow_thousands_extra_digits is True,
                    self.allow_thousands_lacking_digits is True,
                    self.allow_decimals_lacking_digits is False,
                ]
            )
            else "Default"
        )

    def __repr__(self) -> str:
        """Return a string representation of the ParserSettings with attributes included."""
        return (
            f'ParserSettings(assume_scale="{self.assume_scale}", '
            f"limit_allowed_terms={self.limit_allowed_terms}, "
            f"allow_duplicate_scales={self.allow_duplicate_scales}, "
            f"allow_thousands_extra_digits={self.allow_thousands_extra_digits}, "
            f"allow_thousands_lacking_digits={self.allow_thousands_lacking_digits}, "
            f"allow_decimals_lacking_digits={self.allow_decimals_lacking_digits})"
        )
