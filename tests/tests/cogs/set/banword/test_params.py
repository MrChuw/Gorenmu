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

    add: ClassVar[list] = [
        pytest.param(
            "en", "Banword(s) added. I will now censor any command that contains it.", marks=pytest.mark.en, id="en"
        ),
        pytest.param(
            "pt_BR",
            "Palavra(s) proibida adicionada. Agora irei censurar qualquer comando que a contenha.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    remove: ClassVar[list] = [
        pytest.param("en", "Banword(s) removed.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "Palavra(s) proibida removida.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    clean: ClassVar[list] = [
        pytest.param("en", "I removed all the banwords words.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "Removi todas as palavras proibidas.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    add_remove: ClassVar[list] = [
        pytest.param(
            "en", "Chose one of the valid options: add, remove or clean. Not None.", marks=pytest.mark.en, id="en"
        ),
        pytest.param(
            "pt_BR",
            "Escolha uma das opções válidas: adicionar, remover ou limpar. Não None.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    what: ClassVar[list] = [
        pytest.param("en", "blablabla", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "blablabla", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]
