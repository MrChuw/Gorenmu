# -*- coding: utf-8 -*-

import pytest


class Params:
    own_user = [
        pytest.param("en", "you're not afk… obviously.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "você não está afk... obviamente.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    bot_nick = [
        pytest.param("en", "I'm always here… watching.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "Estou sempre aqui... assistindo.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    no_content = [
        pytest.param("en", "@status_user_50 it's afk 🏃⌨", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "@status_user_50 está ausente 🏃⌨", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    content = [
        pytest.param("en", "@status_user_51 it's afk 🏃⌨ and left a note: content", marks=pytest.mark.en, id="en"),
        pytest.param(
            "pt_BR", "@status_user_51 está ausente 🏃⌨ e deixou uma nota: content", marks=pytest.mark.pt_BR, id="pt_BR"
        ),
    ]

    user_dont_exist = [
        pytest.param("en", "I don't remember ever seeing any @not_user_1234.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "Não me lembro de ter visto nenhum @not_user_1234.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]
