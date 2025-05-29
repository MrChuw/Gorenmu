# -*- coding: utf-8 -*-

import pytest


class Params:
    content = [
        pytest.param("en", "albalbalb", marks=pytest.mark.en, id="en"),  # NOQA
        pytest.param("pt_BR", "albalbalb", marks=pytest.mark.pt_BR, id="pt_BR"),  # NOQA
    ]
