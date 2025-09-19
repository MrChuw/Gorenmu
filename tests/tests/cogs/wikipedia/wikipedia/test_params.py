# -*- coding: utf-8 -*-

import pytest


class Params:
    decorators = [
        pytest.param("en", "Sends a random wikipedia.", "To use: +wikihow", marks=pytest.mark.en, id="en"),
        pytest.param(
            "pt_BR", "Envia uma wikipedia aleatória.", "Para usar: +wikihow", marks=pytest.mark.pt_BR, id="pt_BR"
        ),
    ]

    two_hundred = [
        pytest.param("en", "www.some_url.com", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "www.some_url.com", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    timeout = [
        pytest.param("en", "It's been 30 seconds and I can't find any valid links.", marks=pytest.mark.en, id="en"),
        pytest.param(
            "pt_BR",
            "Já se passaram 30 segundos e não consegui encontrar nenhum link válido.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    exception = [
        pytest.param("en", "An error occurred, please try again: fail", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "Ocorreu um erro. Tente novamente: fail", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]
