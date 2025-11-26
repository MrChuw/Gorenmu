from typing import ClassVar

import pytest


class Params:
    decorators: ClassVar[list] = [
        pytest.param(
            "en",
            "Shows a user's Twitch profile image.",
            "How to use: +profilepicture (username)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Mostra a imagem de perfil de um usuário da Twitch.",
            "Como usar: +profilepicture (nome_de_usuário)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    success: ClassVar[list] = [
        pytest.param(
            "en",
            "https://short.url/profile  https://short.url/pic",
            marks=pytest.mark.en,
            id="success-en",
        ),
        pytest.param(
            "pt_BR",
            "https://short.url/profile  https://short.url/pic",
            marks=pytest.mark.pt_BR,
            id="success-pt",
        ),
    ]

    not_found: ClassVar[list] = [
        pytest.param(
            "en",
            "I couldn't find any user named @unknown_user.",
            marks=pytest.mark.en,
            id="not_found-en",
        ),
        pytest.param(
            "pt_BR",
            "Não consegui encontrar nenhum usuário chamado @unknown_user.",
            marks=pytest.mark.pt_BR,
            id="not_found-pt",
        ),
    ]
