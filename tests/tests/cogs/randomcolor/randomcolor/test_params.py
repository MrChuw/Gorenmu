# -*- coding: utf-8 -*-

import pytest


class Params:
    no_tipo = [
        pytest.param(
            "en", "#C53EDF is Medium Purple. https://color.mrchuw.com.br/hex/c53edf", marks=pytest.mark.en, id="en"
        ),
        pytest.param(
            "pt_BR",
            "#C53EDF é Medium Purple. https://color.mrchuw.com.br/hex/c53edf",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    hex_tipo = [
        pytest.param(
            "en", "#C53EDF is Medium Purple. https://color.mrchuw.com.br/hex/c53edf", marks=pytest.mark.en, id="en"
        ),
        pytest.param(
            "pt_BR",
            "#C53EDF é Medium Purple. https://color.mrchuw.com.br/hex/c53edf",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    hex_name_api_down = [
        pytest.param(
            "en",
            "#C53EDF is thecolorapi.com is inaccessible. https://color.mrchuw.com.br/hex/c53edf",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "#C53EDF é thecolorapi.com esta inacessível. https://color.mrchuw.com.br/hex/c53edf",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    rgb_name_api_down = [
        pytest.param(
            "en",
            "#C5D714 is thecolorapi.com is inaccessible. https://color.mrchuw.com.br/rgb/197,215,20",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "#C5D714 é thecolorapi.com esta inacessível. https://color.mrchuw.com.br/rgb/197,215,20",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]
