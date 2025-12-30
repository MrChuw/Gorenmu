from typing import ClassVar

import pytest


class Params:
    decorators: ClassVar[list] = [
        pytest.param(
            "en",
            "Transform user ID into username and vice versa.",
            "To use: +userid (username/id)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Transformar o id do usuário em nome de usuário e vice-versa.",
            "Para usar: +userid (username/id)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]
    no_content: ClassVar[list] = [
        pytest.param("en", "1234", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "1234", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    invalid_user: ClassVar[list] = [
        pytest.param("en", "Invalid username: @some_user", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "Nome de usuário inválido: @some_user", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    no_user: ClassVar[list] = [
        pytest.param("en", "I couldn't find any user named @some_user.", marks=pytest.mark.en, id="en"),
        pytest.param(
            "pt_BR", "Não consegui encontrar nenhum usuário chamado @some_user.", marks=pytest.mark.pt_BR, id="pt_BR"
        ),
    ]

    no_id: ClassVar[list] = [
        pytest.param("en", "I couldn't find any user with id 123456.", marks=pytest.mark.en, id="en"),
        pytest.param(
            "pt_BR", "Não consegui encontrar nenhum usuário com id 123456.", marks=pytest.mark.pt_BR, id="pt_BR"
        ),
    ]

    invalid_id: ClassVar[list] = [
        pytest.param("en", "Invalid id: 123456", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "ID inválido: 123456", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]
