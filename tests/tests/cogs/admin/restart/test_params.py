from typing import ClassVar

import pytest


class Params:
    decorators: ClassVar[list] = [
        pytest.param("en", "Restarts the bot.", "To use: +restart", marks=pytest.mark.en, id="en"),
        pytest.param(
            "pt_BR",
            "Reinicia o bot.",
            "Para usar: +restart",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    success: ClassVar[list] = [
        pytest.param("en", "", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    failure: ClassVar[list] = [
        pytest.param(
            "en",
            "There was an error restarting the bot: exec failed",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Um erro aconteceu ao reiniciar o bot: exec failed",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]
