# -*- coding: utf-8 -*-

import pytest


class Params:
    decorators = [
        pytest.param("en", "User nickname history.", "To use: +nicks (user nick)", marks=pytest.mark.en, id="en"),
        pytest.param(
            "pt_BR",
            "Histórico de nicks de um usuário.",
            "Para usar: +nicks (nick do usuário)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    no_content = [
        pytest.param("en", "blablabla", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "blablabla", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    params_ = [
        pytest.param("en", "blablabla", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "blablabla", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]
