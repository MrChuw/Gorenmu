from typing import ClassVar

import pytest


class Params:
    decorators: ClassVar[list] = [
        pytest.param(
            "en",
            "Command used to add ban words that the bot cannot send in the chat.",
            "To use: +set banword (add|remove|clean) (words)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Comando usado para adicionar palavras proibidas que o bot não pode enviar no chat.",
            "Para usar: +set banword (add|remove|clean) (palavras)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    no_content: ClassVar[list] = [
        pytest.param("en", "blablabla", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "blablabla", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    changed: ClassVar[list] = [
        pytest.param("en", "Prefix changed to -", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "Prefixo alterado para -", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    to_long: ClassVar[list] = [
        pytest.param("en", "The prefix --- is too long, please keep it shorter than 2.", marks=pytest.mark.en, id="en"),
        pytest.param(
            "pt_BR",
            "O prefixo --- é muito longo, por favor, mantenha-o mais curto que 2.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    params_: ClassVar[list] = [
        pytest.param("en", "blablabla", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "blablabla", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]
