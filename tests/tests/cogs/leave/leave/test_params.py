from typing import ClassVar

import pytest


class Params:
    decorators: ClassVar[list] = [
        pytest.param(
            "en",
            "This command is used to remove the bot from your chat.",
            "To use: +leave",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Este comando é usado para remover o bot do seu chat.",
            "Para usar: +leave",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]
    not_in_channel: ClassVar[list] = [
        pytest.param("en", "I'm not on your channel.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "Eu não estou no seu canal.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    channel_removed: ClassVar[list] = [
        pytest.param("en", "I'm not on your channel.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "Eu não estou no seu canal.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    on_channel: ClassVar[list] = [
        pytest.param("en", "Your channel @username has been successfully removed.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "Seu canal @username foi removido com sucesso.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]
