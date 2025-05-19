# -*- coding: utf-8 -*-
import pytest


params_alias = [
    pytest.param("en", ["", 1, "Shush"], marks=pytest.mark.en, id="en"),
    pytest.param("pt_BR", ["", 1, "Shush"], marks=pytest.mark.pt_BR, id="pt_BR"),
]
