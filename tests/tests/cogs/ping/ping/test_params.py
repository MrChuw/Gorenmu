# -*- coding: utf-8 -*-

import pytest


class Params:
    decorators = [
        pytest.param("en", "", "", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "", "", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]
    pong = [
        pytest.param(
            "en",
            r"^pong 🏓 \|\| TMI: \d+\.\d+ ms \|\| RAM: \d+\.\d+ MB \|\| \d+\.\d+ seconds?$",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            r"^pong 🏓 \|\| TMI: \d+\.\d+ ms \|\| RAM: \d+\.\d+ MB \|\| \d+\.\d+ segundo[s]?$",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    ping = [
        pytest.param(
            "en",
            r"^ping 🏓 \|\| TMI: \d+\.\d+ ms \|\| RAM: \d+\.\d+ MB \|\| \d+\.\d+ seconds?$",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            r"^ping 🏓 \|\| TMI: \d+\.\d+ ms \|\| RAM: \d+\.\d+ MB \|\| \d+\.\d+ segundo[s]?$",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]
