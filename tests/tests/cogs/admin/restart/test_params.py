# -*- coding: utf-8 -*-
import pytest


class Params:
    decorators = [
        pytest.param("en", "Restarts the bot.", "To use: +restart", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "Reinicia o bot.", "Para usar: +restart", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    success = [
        pytest.param("en", "", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    failure = [
        pytest.param("en", "There was an error restarting the bot: exec failed", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "Um erro aconteceu ao reiniciar o bot: exec failed", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]
