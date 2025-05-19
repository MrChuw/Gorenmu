# -*- coding: utf-8 -*-

import pytest


class Params:

    no_content = [
        pytest.param(
            "en",
            "List of your aliases: The_Tests_alias | Detailed list: https://shlink.mrchuw.com.br/uQqt5",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Lista dos seus aliases: The_Tests_alias | Lista detalhada: https://shlink.mrchuw.com.br/uQqt5",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    no_match_and_no_second_name = [
        pytest.param("en", "User some_user_44 has no registered aliases.", marks=pytest.mark.en, id="en"),
        pytest.param(
            "pt_BR", "O usuário some_user_44 não possui aliases registrados.", marks=pytest.mark.pt_BR, id="pt_BR"
        ),
    ]

    alias_match_without_second_name = [
        pytest.param(
            "en",
            "The_Tests_alias || Invoke: chance  || Link: https://shlink.mrchuw.com.br/uQqt5",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "The_Tests_alias || Invoca: chance  || Link: https://shlink.mrchuw.com.br/uQqt5",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    check_user = [
        pytest.param(
            "en", "List of @some_user_45 aliases: https://shlink.mrchuw.com.br/uQqt5", marks=pytest.mark.en, id="en"
        ),
        pytest.param(
            "pt_BR",
            "Lista de aliases de @some_user_45: https://shlink.mrchuw.com.br/uQqt5",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    special_case = [
        pytest.param(
            "en",
            "Special case!\n "
            'Your alias "The_Tests_user": https://shlink.mrchuw.com.br/uQqt5\n '
            "List of The_Tests_user's aliases: https://shlink.mrchuw.com.br/uQqt5",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Caso especial!\n"
            'Seu alias "The_Tests_user": https://shlink.mrchuw.com.br/uQqt5\n'
            "Lista dos aliases de The_Tests_user: https://shlink.mrchuw.com.br/uQqt5",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    search_alias_on_user = [
        pytest.param(
            "en",
            "The_Alias_test || Invoke: chance  || Link: https://shlink.mrchuw.com.br/uQqt5",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "The_Alias_test || Invoca: chance  || Link: https://shlink.mrchuw.com.br/uQqt5",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    search_wrong_alias_on_user = [
        pytest.param(
            "en", '@The_Tests_user don\'t have the "The_Wrong_Alias_test" alias!', marks=pytest.mark.en, id="en"
        ),
        pytest.param(
            "pt_BR", '@The_Tests_user não tem o alias "The_Wrong_Alias_test"!', marks=pytest.mark.pt_BR, id="pt_BR"
        ),
    ]

    search_deleted_alias_on_user = [
        pytest.param(
            "en",
            "The_Deleted_Alias_test alias is a link to a different alias, but the original has been deleted.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "The_Deleted_Alias_test alias é um link para um alias diferente, mas o original foi excluído.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]
