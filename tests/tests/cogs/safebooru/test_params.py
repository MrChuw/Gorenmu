# -*- coding: utf-8 -*-

import pytest


class Params:
    decorators = [
        pytest.param(
            "en",
            "Command used to generate random images from Safebooru.",
            "To use: {}safebooru (tags)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Comando usado para gerar imagens aleatórias de Safebooru.",
            "Para usar: {}safebooru (tags)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]
    no_content = [
        pytest.param("en", "Original: www.some_url.com || Preview: www.some_url.com", marks=pytest.mark.en, id="en"),
        pytest.param(
            "pt_BR", "Original: www.some_url.com || Preview: www.some_url.com", marks=pytest.mark.pt_BR, id="pt_BR"
        ),
    ]
