from typing import ClassVar

import pytest


class Params:
    decorators: ClassVar[list] = [
        pytest.param("en", "", "", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "", "", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    pong: ClassVar[list] = [
        pytest.param(
            "en",
            r"^pong 🏓 \|\| TMI: \d+(\.\d+)? ms \|\| RAM: \d+(\.\d+)? MB \|\| \d+ days?$",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            r"^pong 🏓 \|\| TMI: \d+(\.\d+)? ms \|\| RAM: \d+(\.\d+)? MB \|\| \d+ dia[s]?$",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    ping: ClassVar[list] = [
        pytest.param(
            "en",
            r"^ping 🏓 \|\| TMI: \d+(\.\d+)? ms \|\| RAM: \d+(\.\d+)? MB \|\| \d+ days?$",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            r"^ping 🏓 \|\| TMI: \d+(\.\d+)? ms \|\| RAM: \d+(\.\d+)? MB \|\| \d+ dia[s]?$",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]
