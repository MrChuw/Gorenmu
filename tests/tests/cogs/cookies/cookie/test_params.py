# -*- coding: utf-8 -*-

import pytest


class Params:
    cookie = [
        pytest.param(
            "en",
            'Choose from one of the options "eat", "count", "top", "gift", "stock" or "sm"',
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            'Escolha entre uma das opções "eat", "count", "top", "gift", "stock" ou "sm"',
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]
