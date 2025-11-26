from typing import ClassVar

import pytest


class Params:
    decorators: ClassVar[list] = [
        pytest.param(
            "en",
            "Repeats the message you send.",
            "+echo (message)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Repete a mensagem que você enviar.",
            "+echo (mensagem)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    no_content: ClassVar[list] = [
        pytest.param("en", "test", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "test", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    punctuation: ClassVar[list] = [
        pytest.param("en", "️@test", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "️@test", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]
