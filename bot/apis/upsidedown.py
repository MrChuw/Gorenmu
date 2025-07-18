# -*- coding: utf-8 -*-

from __future__ import unicode_literals

__all__ = ["transform"]
__version__ = "0.4"
__author__ = "Christoph Burgmer <christoph.burgmer@gmail.com>"
__url__ = "http://github.com/cburgmer/upsidedown"
__license__ = "MIT"

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
"""

import string

import unicodedata

FLIP_RANGES = [
    (string.ascii_lowercase, "ɐqɔpǝɟƃɥᴉɾʞꞁɯuodbɹsʇnʌʍxʎz"),  # NOQA
    (string.ascii_uppercase, "ⱯᗺƆᗡƎᖵ⅁HIᒋ⋊ꞀWNOԀꝹᴚS⊥∩ɅMX⅄Z"),  # NOQA
    (string.digits, "0ІᘔƐᔭ59Ɫ86"),
    (string.punctuation, "¡„#$%⅋,)(*+'-˙/:؛>=<¿@]\\[ᵥ‾`}|{~"),
]
UNICODE_COMBINING_DIACRITICS = {
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

TRANSLITERATIONS = {"ß": "ss"}

_CHARLOOKUP = {}
for chars, flipped in FLIP_RANGES:
    _CHARLOOKUP |= zip(chars, flipped)

for char in _CHARLOOKUP.copy():
    assert (
        _CHARLOOKUP[char] not in _CHARLOOKUP or _CHARLOOKUP[_CHARLOOKUP[char]] == char
    ), f"{_CHARLOOKUP[char]} has ambiguous mapping"
    _CHARLOOKUP[_CHARLOOKUP[char]] = char

_DIACRITICSLOOKUP = (
    dict([(UNICODE_COMBINING_DIACRITICS[char], char) for char in UNICODE_COMBINING_DIACRITICS])
    | UNICODE_COMBINING_DIACRITICS
)


def transform(string_: str, transliterations=None):
    """
    Transform the string to "upside-down" writing.

    Example:

        >>> import bot.apis.upsidedown
        >>> print(upsidedown.transform('Hello World!')) # NOQA
        ¡pꞁɹoM oꞁꞁǝH

    For languages with diacritics you might want to supply a transliteration to
    work around missing (rendering of) upside-down forms:
        >>> import bot.apis.upsidedown
        >>> print(upsidedown.transform('köln',transliterations={'ö': 'oe'})) # NOQA
        uꞁǝoʞ
    """
    transliterations = transliterations or TRANSLITERATIONS

    for character in transliterations:
        string_ = string_.replace(character, transliterations[character])

    input_chars = list(string_)
    input_chars.reverse()

    output = []
    for character in input_chars:
        if character in _CHARLOOKUP:
            output.append(_CHARLOOKUP[character])
        else:
            char_normalised = unicodedata.normalize("NFD", character)

            for c in char_normalised[:]:
                if c in _CHARLOOKUP:
                    char_normalised = char_normalised.replace(c, _CHARLOOKUP[c])
                elif c in _DIACRITICSLOOKUP:
                    char_normalised = char_normalised.replace(c, _DIACRITICSLOOKUP[c])

            output.append(unicodedata.normalize("NFC", char_normalised))

    return "".join(output)
