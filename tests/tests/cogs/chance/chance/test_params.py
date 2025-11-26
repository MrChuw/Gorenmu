from typing import ClassVar

import pytest


class Params:
    decorators: ClassVar[list] = [
        pytest.param(
            "en",
            "Returns a random percentage.",
            "To use: +chance",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Retorna uma porcentagem aleatória.",
            "Para usar: +chance",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    chance: ClassVar[list] = [
        pytest.param("en", "84.44%", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "84.44%", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]
