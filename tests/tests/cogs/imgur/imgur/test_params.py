from typing import ClassVar

import pytest


class Params:
    decorators: ClassVar[list] = [
        pytest.param(
            "en",
            "Command used to generate random images from Imgur. NSFW command disabled by default.",
            "To use: +imgur(7) (amount)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Comando usado para gerar imagens aleatórias do Imgur. O comando NSFW está desativado por padrão.",
            "Para usar: +imgur(7) (quantidade)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    # no_content: ClassVar[list] = [
    #     pytest.param("en", "blablabla", marks=pytest.mark.en, id="en"),
    #     pytest.param("pt_BR", "blablabla", marks=pytest.mark.pt_BR, id="pt_BR"),
    # ]
    #
    # params_: ClassVar[list] = [
    #     pytest.param("en", "blablabla", marks=pytest.mark.en, id="en"),
    #     pytest.param("pt_BR", "blablabla", marks=pytest.mark.pt_BR, id="pt_BR"),
    # ]
    #
    # params_: ClassVar[list] = [
    #     pytest.param("en", "blablabla", marks=pytest.mark.en, id="en"),
    #     pytest.param("pt_BR", "blablabla", marks=pytest.mark.pt_BR, id="pt_BR"),
    # ]
    #
    # params_: ClassVar[list] = [
    #     pytest.param("en", "blablabla", marks=pytest.mark.en, id="en"),
    #     pytest.param("pt_BR", "blablabla", marks=pytest.mark.pt_BR, id="pt_BR"),
    # ]
