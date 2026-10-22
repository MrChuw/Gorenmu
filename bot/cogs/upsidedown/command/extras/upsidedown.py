from __future__ import annotations

import string
import unicodedata
from collections.abc import Mapping
from typing import Final

__all__ = ["transform"]

"""
Copyright (c) 2008-2010 Christoph Burgmer

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

__version__ = "modified"
__author__ = "Christoph Burgmer <christoph.burgmer@gmail.com>"
__url__ = "http://github.com/cburgmer/upsidedown"
__license__ = "MIT"
"""


FLIP_RANGES: Final[list[tuple[str, str]]] = [
    (string.ascii_lowercase, "ɐqɔpǝɟƃɥᴉɾʞꞁɯuodbɹsʇnʌʍxʎz"),  # noqa: RUF001
    (string.ascii_uppercase, "ⱯᗺƆᗡƎᖵ⅁HIᒋ⋊ꞀWNOԀꝹᴚS⊥∩ɅMX⅄Z"),
    (string.digits, "0ІᘔƐᔭ59Ɫ86"),  # noqa: RUF001
    (string.punctuation, "¡„#$%⅋,)(*+'-˙/:؛>=<¿@]\\[ᵥ‾`}|{~"),
]

EXTRA_FLIP_PAIRS: Final[list[tuple[str, str]]] = [
    ("‘", "’"),  # noqa: RUF001
    ("“", "”"),
    ("‚", "‛"),  # noqa: RUF001
    ("—", "—"),
    ("–", "–"),  # noqa: RUF001
    ("…", "…"),
    ("°", "°"),
    ("§", "§"),
    ("×", "×"),  # noqa: RUF001
    ("÷", "÷"),
    ("†", "†"),
]

UNICODE_COMBINING_DIACRITICS: Final[dict[str, str]] = {
    "̈": "̤",
    "̊": "̥",
    "́": "̗",
    "̀": "̖",
    "̇": "̣",
    "̃": "̰",
    "̄": "̱",
    "̂": "̬",
    "̆": "̯",
    "̌": "̭",
    "̑": "̮",
    "̍": "̩",
}

TRANSLITERATIONS: Final[dict[str, str]] = {
    "ß": "ss",
    "æ": "ae",
    "Æ": "AE",
    "œ": "oe",
    "Œ": "OE",
    "ø": "o",
    "Ø": "O",
    "ð": "d",
    "Ð": "D",
    "þ": "th",
    "Þ": "TH",
    "ł": "l",
    "Ł": "L",
    "đ": "d",
    "Đ": "D",
    "ħ": "h",
    "Ħ": "H",
    "ŋ": "n",
    "Ŋ": "N",
    "ı": "i",  # noqa: RUF001
    "İ": "I",
    "ĳ": "ij",
    "Ĳ": "IJ",
}

_BRAILLE_ROTATION_MAP = {0: 7, 1: 4, 2: 3, 3: 2, 4: 1, 5: 6, 6: 5, 7: 0}

_BRAILLE_LOOKUP: dict[str, str] = {}
for _code in range(0x2800, 0x2900):
    _src_char = chr(_code)
    _pattern = _code - 0x2800
    _rot_pattern = sum(
        1 << _dst_bit for _src_bit, _dst_bit in _BRAILLE_ROTATION_MAP.items() if (_pattern >> _src_bit) & 1
    )
    _BRAILLE_LOOKUP[_src_char] = chr(0x2800 + _rot_pattern)

_CHARLOOKUP: dict[str, str] = {}
for _chars, _flipped in FLIP_RANGES:
    _CHARLOOKUP |= zip(_chars, _flipped, strict=True)

for _left, _right in EXTRA_FLIP_PAIRS:
    _CHARLOOKUP.setdefault(_left, _right)
    _CHARLOOKUP.setdefault(_right, _left)

_CHARLOOKUP |= _BRAILLE_LOOKUP

for _char in list(_CHARLOOKUP):
    _mapped = _CHARLOOKUP[_char]
    if _mapped not in _CHARLOOKUP:
        _CHARLOOKUP[_mapped] = _char

_DIACRITICSLOOKUP: Final[dict[str, str]] = {
    UNICODE_COMBINING_DIACRITICS[char]: char for char in UNICODE_COMBINING_DIACRITICS
} | UNICODE_COMBINING_DIACRITICS

_TRANSLATE_TABLE: Final[dict[int, str]] = {ord(char): flipped for char, flipped in _CHARLOOKUP.items()}


def _flip_char(character: str) -> str:
    char_normalised = unicodedata.normalize("NFD", character)

    for component in char_normalised[:]:
        if component in _CHARLOOKUP:
            char_normalised = char_normalised.replace(component, _CHARLOOKUP[component])
        elif component in _DIACRITICSLOOKUP:
            char_normalised = char_normalised.replace(component, _DIACRITICSLOOKUP[component])

    return unicodedata.normalize("NFC", char_normalised)


def _flip_line(line: str) -> str:
    output: list[str] = []
    for character in reversed(line):
        flipped = _TRANSLATE_TABLE.get(ord(character))
        output.append(flipped if flipped is not None else _flip_char(character))
    return "".join(output)


def transform(string_: str, transliterations: Mapping[str, str] | None = None) -> str:
    """Transform the string to "upside-down" writing.

    Example:

        >>> import upsidedown
        >>> print(upsidedown.transform("Hello World!"))  # NOQA
        ¡pꞁɹoM oꞁꞁǝH

    For languages with diacritics or letters that have no legible
    upside-down glyph you can supply (or extend) the transliteration map:

        >>> import upsidedown
        >>> print(upsidedown.transform("köln", transliterations={"ö": "oe"}))  # NOQA
        uꞁǝoʞ

    :param string_: the text to flip.
    :param transliterations: mapping applied before flipping, replacing
        characters with no good upside-down glyph. Defaults to
        `TRANSLITERATIONS`; pass your own mapping to extend or override it,
        e.g. ``{**TRANSLITERATIONS, "ö": "oe"}``.
    """
    active_transliterations: Mapping[str, str] = transliterations if transliterations is not None else TRANSLITERATIONS

    for character, replacement in active_transliterations.items():
        string_ = string_.replace(character, replacement)

    # Inverte de baixo para cima as linhas e da direita para a esquerda cada linha
    lines = string_.split("\n")
    return "\n".join(_flip_line(line) for line in reversed(lines))
