from typing import ClassVar

import pytest


class Params:
    decorators: ClassVar[list] = [
        pytest.param(
            "en",
            "Type the command and the user's name to see if they are AFK.",
            "How to use: +IsAfk (username)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Digite o comando e o nome do usuário para ver se eles são AFK.",
            "Como usar: +IsAfk (nome de usuário)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    own_user: ClassVar[list] = [
        pytest.param("en", "you're not afk… obviously.", marks=pytest.mark.en, id="en"),
        pytest.param(
            "pt_BR",
            "você não está afk... obviamente.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    bot_nick: ClassVar[list] = [
        pytest.param("en", "I'm always here… watching.", marks=pytest.mark.en, id="en"),
        pytest.param(
            "pt_BR",
            "Estou sempre aqui... assistindo.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    no_content: ClassVar[list] = [
        pytest.param(
            "en",
            "@status_user_50 it's afk 🏃⌨ (for 1 day)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            '@status_user_50 está ausente 🏃⌨ (há 1 dia)',
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    content: ClassVar[list] = [
        pytest.param(
            "en",
            "@status_user_51 it's afk 🏃⌨ and left a note: content (for 1 day)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            '@status_user_51 está ausente 🏃⌨ e deixou uma nota: content (há 1 dia)',
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    user_dont_exist: ClassVar[list] = [
        pytest.param(
            "en",
            "I don't remember ever seeing any @not_user_1234.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Não me lembro de ter visto nenhum @not_user_1234.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]
