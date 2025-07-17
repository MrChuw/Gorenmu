# -*- coding: utf-8 -*-

import pytest


class Params:
    decorators = [
        pytest.param(
            "en",
            "Translates a text into random languages depending on how many times the user requests.",
            "To use: {}hypertranslate (number of times) text",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Traduzir um texto em idiomas aleatórios dependendo de quantas vezes o usuário solicita.",
            "Para usar: {}hypertranslate (número de vezes) texto",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]
    text = [
        pytest.param("en", "Some_Text", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "Some_Text", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    text_and_quantity = [
        pytest.param("en", "Some Nice Text", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "Some Nice Text", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]
