# -*- coding: utf-8 -*-
import pytest


class Params:
    decorators = [
        pytest.param(
            "en",
            "Type the command and the user's name to see if they are AFK.",
            "How to use: {}IsAfk (username)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Digite o comando e o nome do usuário para ver se eles são AFK.",
            "Como usar: {}IsAfk (nome de usuário)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    own_user = [
        pytest.param("en", "you're not afk… obviously.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "você não está afk... obviamente.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    bot_nick = [
        pytest.param("en", "I'm always here… watching.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "Estou sempre aqui... assistindo.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    no_content = [
        pytest.param("en", r"it's afk 🏃⌨ \(for \d+\.\d{2} seconds\)", marks=pytest.mark.en, id="en"),
        pytest.param(
            "pt_BR", r"@status_user_50 está ausente 🏃⌨ \(há \d+\.\d{2} seconds\)", marks=pytest.mark.pt_BR, id="pt_BR"
        ),
    ]

    content = [
        pytest.param(
            "en",
            r"@status_user_51 it's afk 🏃⌨ and left a note: content \(for \d+\.\d{2} seconds\)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            r"@status_user_51 está ausente 🏃⌨ e deixou uma nota: content \(há \d+\.\d{2} seconds\)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    user_dont_exist = [
        pytest.param("en", "I don't remember ever seeing any @not_user_1234.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "Não me lembro de ter visto nenhum @not_user_1234.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]
