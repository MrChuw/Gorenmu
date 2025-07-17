# -*- coding: utf-8 -*-

import pytest


class Params:
    decorators = [
        pytest.param(
            "en", "Turns the text upside down.", "To use: {}upsidedown (message)", marks=pytest.mark.en, id="en"
        ),
        pytest.param(
            "pt_BR",
            "Vira o texto de cabeça para baixo.",
            "Para usar: {}upsidedown <texto>",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    content = [
        pytest.param("en", "ʇxƎ⊥ ǝɯos", marks=pytest.mark.en, id="en"),  # NOQA
        pytest.param("pt_BR", "ʇxƎ⊥ ǝɯos", marks=pytest.mark.pt_BR, id="pt_BR"),  # NOQA
    ]
