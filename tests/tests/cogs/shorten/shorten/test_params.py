from typing import ClassVar

import pytest


class Params:
    decorators: ClassVar[list] = [
        pytest.param(
            "en",
            "Shorten links using my link shortening service.",
            "To use: +shorten (links)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Encurta links usando o meu serviço de encurtar links.",
            "Para usar: +shorten (links)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    one_link: ClassVar[list] = [
        pytest.param("en", "Here is the URL: https://success.url/", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "Aqui está URL: https://success.url/", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    multiple_links: ClassVar[list] = [
        pytest.param(
            "en",
            "Here are all the URLs: https://success.url/ https://success.url/ https://success.url/ ",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Aqui estão todos os URLs: https://success.url/ https://success.url/ https://success.url/ ",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    error_link: ClassVar[list] = [
        pytest.param("en", "The shortener API is currently experiencing issues.", marks=pytest.mark.en, id="en"),
        pytest.param(
            "pt_BR", "A API do encurtador apresentando problemas no momento.", marks=pytest.mark.pt_BR, id="pt_BR"
        ),
    ]

    json_success: ClassVar[dict] = {"shortUrl": "https://success.url/"}

    json_error: ClassVar[dict] = {"status": "error"}
