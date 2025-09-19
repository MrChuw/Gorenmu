# -*- coding: utf-8 -*-

import pytest


class Params:
    decorators = [
        pytest.param(
            "en",
            "Main command to customize your user settings.",
            "Usage: +set (subcommand) [arguments]",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Comando principal para personalizar suas configurações de usuário.",
            "Uso: +set (subcomando) [argumentos]",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    set_base = [
        pytest.param("en", "", "", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "", "", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]
