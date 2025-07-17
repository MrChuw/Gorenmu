# -*- coding: utf-8 -*-

import pytest


class Params:
    decorators = [
        pytest.param("en", "Reverses a text.", "To use: {}reverse (text)", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "Inverte um texto.", "Para usar: {}reverse <texto>", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    content = [
        pytest.param("en", "albalbalb", marks=pytest.mark.en, id="en"),  # NOQA
        pytest.param("pt_BR", "albalbalb", marks=pytest.mark.pt_BR, id="pt_BR"),  # NOQA
    ]
