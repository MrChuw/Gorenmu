# -*- coding: utf-8 -*-

import pytest


class Params:
    decorators = [
        pytest.param(
            "en",
            "This subcommand is used to delete an alias.",
            "How to use: +alias remove (alias)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Este subcomando é usado para excluir um alias.",
            "Como usar: +alias remove (alias)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]
    no_content = [
        pytest.param("en", "No alias name provided!", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "Nenhum nome de alias fornecido!", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    remove_no_alias = [
        pytest.param("en", 'You don\'t have the "Some_Alias" alias!', marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", 'Você não tem o alias "Some_Alias"!', marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    remove_success = [
        pytest.param(
            "en", 'Your alias "The_Tests_alias" has been successfully removed.', marks=pytest.mark.en, id="en"
        ),
        pytest.param(
            "pt_BR", 'Seu alias "The_Tests_alias" foi removido com sucesso.', marks=pytest.mark.pt_BR, id="pt_BR"
        ),
    ]
