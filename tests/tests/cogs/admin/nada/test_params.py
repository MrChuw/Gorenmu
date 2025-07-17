# pqp -*- coding: utf-8 -*-
import pytest


class Params:
    decorators = [
        pytest.param(
            "en", "This command is used for testing.", "How to use: {}nada (text)", marks=pytest.mark.en, id="en"
        ),
        pytest.param(
            "pt_BR",
            "Este comando é usado para testes.",
            "Como usar: {}nada (text)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    nada = [
        pytest.param("en", "The command was executed successfully.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "O comando foi executado com sucesso.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]
