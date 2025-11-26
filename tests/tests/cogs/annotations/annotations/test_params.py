from typing import ClassVar

import pytest


class Params:
    decorators: ClassVar[list] = [
        pytest.param(
            "en",
            "Creates permanent notes for the user.",
            "To use: +note add/check/delete",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Cria notas permanentes para o usuário.",
            "Para usar: +note add/check/delete",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    annotations: ClassVar[list] = [
        pytest.param("en", ["", 1, "Shush"], marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", ["", 1, "Shush"], marks=pytest.mark.pt_BR, id="pt_BR"),
    ]
