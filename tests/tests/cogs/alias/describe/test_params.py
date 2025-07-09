# -*- coding: utf-8 -*-

import pytest


class Params:
    decorators = [
        pytest.param(
            "en",
            "This subcommand is used to check infos for an alias.",
            "How to use: {}alias description cool_name (new description)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Este subcomando é usado para adicionar ou verificar a descrição de um alias.",
            "Como usar: {}alias description cool_name (nova descrição)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    no_content = [
        pytest.param(
            "en",
            "You didn't provide a alias or description! Use: +alias describe (name) (…description)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Você não forneceu um alias ou uma descrição! Use: +alias describe (nome) (…descrição)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    wrong_alias_no_description = [
        pytest.param("en", 'You don\'t have the "Some_alias" alias!', marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", 'Você não tem o alias "Some_alias"!', marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    alias_no_description = [
        pytest.param(
            "en",
            'The description of alias "The_Tests_alias" has been reset successfully.',
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            'A descrição do alias "The_Tests_alias" foi removida com sucesso.',
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    alias_description = [
        pytest.param(
            "en",
            'The description of alias "The_Tests_alias" has been updated successfully.',
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            'A descrição do alias "The_Tests_alias" foi atualizada com sucesso.',
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]
