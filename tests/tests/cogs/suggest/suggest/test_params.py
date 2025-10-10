# -*- coding: utf-8 -*-

import pytest


class Params:
    decorators = [
        pytest.param(
            "en", "suggest a new feature to the Bot.", "To use: +suggest (description)", marks=pytest.mark.en, id="en"
        ),
        pytest.param(
            "pt_BR",
            "sugerir um novo recurso para o Bot.",
            "Para usar: +suggest (descrição)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]
    no_content = [
        pytest.param("en", "blablabla", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "blablabla", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    params_ = [
        pytest.param("en", "blablabla", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "blablabla", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]
