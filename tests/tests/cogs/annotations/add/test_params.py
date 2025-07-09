# -*- coding: utf-8 -*-

import pytest


class Params:
    decorators = [
        pytest.param(
            "en",
            "This subcommand is used to add an note.",
            "How to use: {}note add (text)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Este subcomando é usado para adicionar uma anotação.",
            "Como usar: {}note add (texto)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    add_no_content = [
        pytest.param("en", "You need to provide content for this command.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "Você precisa fornecer conteúdo para este comando.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    add_content_no_title = [
        pytest.param("en", "Note successfully created. 📝 (ID: 1)", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "Nota criada com sucesso. 📝 (ID: 1)", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    add_content_too_long_no_title = [
        pytest.param("en", "The message must have a maximum of 450 characters.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "A mensagem deve ter no máximo 450 caracteres.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    add_content_title = [
        pytest.param("en", "Note successfully created. 📝 (ID: 1)", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "Nota criada com sucesso. 📝 (ID: 1)", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    add_content_title_too_long = [
        pytest.param("en", "The title must have a maximum of 32 characters.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "O título deve ter um máximo de 32 caracteres.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]
