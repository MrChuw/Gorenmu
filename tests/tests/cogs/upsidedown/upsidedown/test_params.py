# -*- coding: utf-8 -*-

import pytest


class Params:
    content = [
        pytest.param("en", "ʇxƎ⊥ ǝɯos", marks=pytest.mark.en, id="en"),  # NOQA
        pytest.param("pt_BR", "ʇxƎ⊥ ǝɯos", marks=pytest.mark.pt_BR, id="pt_BR"),  # NOQA
    ]
