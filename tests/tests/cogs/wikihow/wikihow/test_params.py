from typing import ClassVar

import pytest


class Params:
    decorators: ClassVar[list] = [
        pytest.param(
            "en",
            "Sends a random wikihow.",
            "To use: +wikihow (amount)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Envia um wikihow aleatório.",
            "Para usar: +wikihow <quantidade>",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    two_hundred: ClassVar[list] = [
        pytest.param("en", "www.some_url.com", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "www.some_url.com", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    timeout: ClassVar[list] = [
        pytest.param(
            "en",
            "It's been 30 seconds and I can't find any valid links.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Já se passaram 30 segundos e não consegui encontrar nenhum link válido.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    exception: ClassVar[list] = [
        pytest.param(
            "en",
            "An error occurred, please try again: fail",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Ocorreu um erro. Tente novamente: fail",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]
