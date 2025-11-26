from typing import ClassVar

import pytest


class Params:
    decorators: ClassVar[list] = [
        pytest.param(
            "en",
            "Sends a random color.",
            "To use: +random_color or add type:hex / type:rgb to specify the type.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Envia uma cor aleatória.",
            "Para usar: +random_color ou adicione type:hex / type:rgb para especificar o tipo.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    no_tipo: ClassVar[list] = [
        pytest.param(
            "en",
            "#C53EDF is Medium Purple. https://color.mrchuw.com.br/hex/c53edf",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "#C53EDF é Medium Purple. https://color.mrchuw.com.br/hex/c53edf",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    hex_tipo: ClassVar[list] = [
        pytest.param(
            "en",
            "#C53EDF is Medium Purple. https://color.mrchuw.com.br/hex/c53edf",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "#C53EDF é Medium Purple. https://color.mrchuw.com.br/hex/c53edf",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    hex_name_api_down: ClassVar[list] = [
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

    rgb_name_api_down: ClassVar[list] = [
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
