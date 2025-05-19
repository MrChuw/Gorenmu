# -*- coding: utf-8 -*-

import pytest


class Params:
    no_content = [
        pytest.param(
            "en", "You must provide both the current alias name and the new one!", marks=pytest.mark.en, id="en"
        ),
        pytest.param("pt_BR", "Você deve fornecer o nome alias atual e o novo!", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    no_alias = [
        pytest.param("en", 'You don\'t have the "Wrong_alias_name" alias!', marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", 'Você não tem o alias "Wrong_alias_name"!', marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    alias_conflict = [
        pytest.param("en", 'You already have the "The_Tests_user" alias!', marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", 'Você já tem o alias "The_Tests_user"!', marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    rename_success = [
        pytest.param(
            "en",
            'Your alias "The_Tests_alias" has been successfully renamed to "The_new_name".',
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            'Seu alias "The_Tests_alias" foi renomeado com sucesso para "The_new_name".',
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]
