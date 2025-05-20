# -*- coding: utf-8 -*-

import pytest


class Params:
    choice_or = [
        pytest.param("en", "1 or 2 or 3", "2", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "1 ou 2 ou 3", "2", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    space = [
        pytest.param("en", "1 2 3", "2", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "1 2 3", "2", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    comma = [
        pytest.param("en", "1, 2, 3", "2", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "1, 2, 3", "2", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    mixed = [
        pytest.param("en", "1 or 2, 3 4", "4", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "1 ou 2, 3 4", "4", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]
