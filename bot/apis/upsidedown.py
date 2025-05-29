#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple module that "flips" latin characters in a string to create an
"upside-down" impression. Makes extensive use of compatible latin characters
encoded in Unicode.

Support for diacritics offered through combining diacritical marks. Depends on
proper rendering though.

2008-2010 Christoph Burgmer (cburgmer@ira.uka.de)
"""


from __future__ import unicode_literals

__all__ = ["transform"]
__version__ = "0.4"
__author__ = "Christoph Burgmer <christoph.burgmer@gmail.com>"
__url__ = "http://github.com/cburgmer/upsidedown"
__license__ = "MIT"

import string

import unicodedata

# Define dual character. Make sure that mapping is bijective.
FLIP_RANGES = [
    (string.ascii_lowercase, "ɐqɔpǝɟƃɥᴉɾʞꞁɯuodbɹsʇnʌʍxʎz"),  # NOQA
    # alternatives: l:ʅ
    (string.ascii_uppercase, "ⱯᗺƆᗡƎᖵ⅁HIᒋ⋊ꞀWNOԀꝹᴚS⊥∩ɅMX⅄Z"),  # NOQA
    # alternatives: L:ᒣ⅂, J:ſ, F:߃Ⅎ, A:∀ᗄ, U:Ⴖ, W:Ϻ, C:ϽↃ, Q:Ό, M:Ɯꟽ
    (string.digits, "0ІᘔƐᔭ59Ɫ86"),
    (string.punctuation, "¡„#$%⅋,)(*+'-˙/:؛>=<¿@]\\[ᵥ‾`}|{~"),
]
# See also http://www.fileformat.info/convert/text/upside-down-map.htm

# See:
# http://de.wikipedia.org/wiki/Unicode-Block_Kombinierende_diakritische_Zeichen
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

# character lookup
_CHARLOOKUP = {}
for chars, flipped in FLIP_RANGES:
    _CHARLOOKUP |= zip(chars, flipped)

# get reverse direction
for char in _CHARLOOKUP.copy():
    # make 1:1 back transformation possible
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
