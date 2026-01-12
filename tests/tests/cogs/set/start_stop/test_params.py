from typing import ClassVar

import pytest


class Params:
    decorators: ClassVar[list] = [
        pytest.param(
            "en",
            "Command used to turn the bot on or off in the chat.",
            "To use: +set start(or on)/stop(or off)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Comando usado para ativar ou desativar o bot no chat.",
            "Para usar: +set start(ou on)/stop(ou off)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    started: ClassVar[list] = [
        pytest.param("en", "The bot was successfully turned on.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "O bot foi ligado com sucesso.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    already_on: ClassVar[list] = [
        pytest.param("en", "The bot is already on.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "O bot já está ligado.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    stopped: ClassVar[list] = [
        pytest.param("en", "The bot was successfully turned off.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "O bot foi desligado com sucesso.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    already_off: ClassVar[list] = [
        pytest.param("en", "The bot is already off.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "O bot já está desligado.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]
