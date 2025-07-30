# -*- coding: utf-8 -*-

import pytest


class Params:
    decorators = [
        pytest.param(
            "en",
            "Set or remove a custom nickname.",
            "Usage: {}set nick <nickname or remove>",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Definir ou remover um apelido personalizado.",
            "Uso: {}set nick <apelido ou remove>",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    nick_set = [
        pytest.param("en", "xXCoolNickNameXx", "Nick changed successfully.", marks=pytest.mark.en, id="nick-en"),
        pytest.param("pt_BR", "xXNickLegalXx", "Apelido alterado com sucesso.", marks=pytest.mark.pt_BR, id="nick-pt"),
    ]

    nick_remove = [
        pytest.param("en", "remove", "Nick removed successfully.", marks=pytest.mark.en, id="remove-en"),
        pytest.param("pt_BR", "remove", "Apelido removido com sucesso.", marks=pytest.mark.pt_BR, id="remove-pt"),
    ]

    nick_too_long = [
        pytest.param("en", "x" * 33, "Nick must be max 32 characters long not 33.", marks=pytest.mark.en, id="long-en"),
        pytest.param(
            "pt_BR",
            "y" * 33,
            "O apelido deve ter no máximo 32 caracteres, e não 33.",
            marks=pytest.mark.pt_BR,
            id="long-pt",
        ),
    ]

    nick_start_punctuation = [
        pytest.param("en", "!alert", "Nick changed successfully.", marks=pytest.mark.en, id="punctuation-en"),
        pytest.param(
            "pt_BR", "#hashtag", "Apelido alterado com sucesso.", marks=pytest.mark.pt_BR, id="punctuation-pt"
        ),
    ]
