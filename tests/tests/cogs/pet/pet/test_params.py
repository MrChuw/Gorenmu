from typing import ClassVar

import pytest


class Params:
    decorators: ClassVar[list] = [
        pytest.param(
            "en",
            "Used to give a pat to one of your pets or see all your pets.",
            "To use: +pet (pet name)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Usado para fazer carinho em um dos seus pets ou ver todos os seus pets.",
            "Para usar: +pet (nome do pet)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    no_content: ClassVar[list] = [
        pytest.param(
            "en", "acquire one of the available pets (+pet buy) in exchange for cookies.", marks=pytest.mark.en, id="en"
        ),
        pytest.param(
            "pt_BR",
            "adquira um dos pets disponíveis (+pet buy) em troca de cookies.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    no_content_but_pet: ClassVar[list] = [
        pytest.param("en", "you has: bee 🐝 | bee2 🐝 | vilão 🦹‍♀️", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "você possui: bee 🐝 | bee2 🐝 | vilão 🦹‍♀️", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    params_: ClassVar[list] = [
        pytest.param("en", "blablabla", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "blablabla", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    params_: ClassVar[list] = [
        pytest.param("en", "blablabla", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "blablabla", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    params_: ClassVar[list] = [
        pytest.param("en", "blablabla", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "blablabla", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]
