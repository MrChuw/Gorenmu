# -*- coding: utf-8 -*-

import pytest


class Params:
    chance = [
        pytest.param("en", "84.44%", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "84.44%", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]
