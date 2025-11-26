from typing import ClassVar

import pytest


class Params:
    no_content: ClassVar[list] = [
        pytest.param("en", "you came back 🏃⌨ (was away for ", marks=pytest.mark.en, id="en"),
        pytest.param(
            "pt_BR",
            "você voltou 🏃⌨ (estava ausente por ",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    not_afk: ClassVar[list] = [
        pytest.param("en", False, marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", False, marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    afk_content: ClassVar[list] = [
        pytest.param(
            "en",
            "you came back 🏃⌨ and left a note: content (was away for",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "você voltou 🏃⌨ e deixou uma nota: content (estava ausente por",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]
