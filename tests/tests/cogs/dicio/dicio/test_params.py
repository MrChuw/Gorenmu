from typing import ClassVar

import pytest


class Params:
    decorators: ClassVar[list] = [
        pytest.param(
            "en",
            "Searches for definitions and information about words in various languages.",
            "+dicio (word) <lang:en>",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Pesquisa definições e informações sobre palavras em diversos idiomas.",
            "+dicio (palavra) <lang:pt_br>",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    exist: ClassVar[list] = [
        pytest.param(
            "en",
            "The word word exist || Similar: a, b, c || Origin: d || Url: https://en.wiktionary.org/wiki/word",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "A palavra word existe || Similares: a, b, c || Origem: d || Url: https://dicio.com.br/word",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    not_exist: ClassVar[list] = [
        pytest.param(
            "en", "The word  does not exist || Similar: a, b, c || Origin:  || Url: ", marks=pytest.mark.en, id="en"
        ),
        pytest.param(
            "pt_BR",
            "A palavra  não existe || Similares: a, b, c || Origem:  || Url: ",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]
