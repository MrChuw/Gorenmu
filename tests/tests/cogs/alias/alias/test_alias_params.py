# -*- coding: utf-8 -*-
import pytest


class Params:
    decorators = [
        pytest.param(
            "en",
            "Command used to manage aliases.",
            "To use: {}alias add|check|copy|describe|edit|link|remove|rename (options)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Comando usado para gerir aliases.",
            "Para usar: {}alias add|check|copy|describe|edit|link|remove|rename (opções)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    params_alias = [
        pytest.param("en", ["", 1, "Shush"], marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", ["", 1, "Shush"], marks=pytest.mark.pt_BR, id="pt_BR"),
    ]
