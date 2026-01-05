from typing import ClassVar

import pytest


class Params:
    decorators: ClassVar[list] = [
        pytest.param(
            "en",
            "This command sends the link to allow the bot to join your chat.",
            "To use: +userid (username/id)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Este comando envia o link que permite ao bot entrar no seu chat.",
            "Para usar: +userid (username/id)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]
    no_content: ClassVar[list] = [
        pytest.param(
            "en", 'https://join.exemple.org/oauth?scopes=channel:bot&force_verify=true ', marks=pytest.mark.en, id="en"
        ),
        pytest.param(
            "pt_BR",
            'https://join.exemple.org/oauth?scopes=channel:bot&force_verify=true ',
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    params_: ClassVar[list] = [
        pytest.param("en", "blablabla", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "blablabla", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]
