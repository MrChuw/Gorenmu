# -*- coding: utf-8 -*-

import pytest


class Params:
    text = [
        pytest.param("en", "Some_Text", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "Some_Text", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    text_and_quantity = [
        pytest.param("en", "Some Nice Text", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "Some Nice Text", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]
