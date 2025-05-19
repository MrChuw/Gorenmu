# -*- coding: utf-8 -*-

import pytest


class Params:
    nada = [
        pytest.param("en", "The command was executed successfully.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "O comando foi executado com sucesso.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]
