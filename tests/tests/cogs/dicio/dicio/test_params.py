# -*- coding: utf-8 -*-

import pytest


class Params:
    decorators = [
        pytest.param("en", "", "+dicio (word) <lang:en>", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "", "+dicio (palavra) <lang:pt_br>", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]
    exist = [
        pytest.param(
            "en",
            "The word word exist || Similar: a, b, c || Origin: d || Url: https://en.wiktionary.org/wiki/word",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "A palavra word existe || Similares: a, b, c  || Origem: d || Url: https://dicio.com.br/word",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    not_exist = [
        pytest.param(
            "en", "The word  does not exist || Similar: a, b, c || Origin:  || Url: ", marks=pytest.mark.en, id="en"
        ),
        pytest.param(
            "pt_BR",
            "A palavra  não existe || Similares: a, b, c  || Origem:  || Url: ",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]
