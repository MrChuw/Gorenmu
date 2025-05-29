# -*- coding: utf-8 -*-

import pytest


class Params:
    no_content = [
        pytest.param(
            "en",
            "There is a total of 0 characters. Of these, 0 are punctuation marks, "
            "0 are uppercase letters, and 0 are special characters.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Há um total de caracteres 0. Destes, 0 são sinais de pontuação, "
            "0 são letras maiúsculas, e 0 são caracteres especiais.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    some_text = [
        pytest.param(
            "en",
            "There is a total of 11 characters. Of these, 1 are punctuation marks, "
            "0 are uppercase letters, and 0 are special characters.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Há um total de caracteres 11. Destes, 1 são sinais de pontuação, "
            "0 são letras maiúsculas, e 0 são caracteres especiais.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    complex_text = [
        pytest.param(
            "en",
            "There is a total of 500 characters. Of these, 129 are punctuation marks, "
            "97 are uppercase letters, and 94 are special characters.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Há um total de caracteres 500. Destes, 129 são sinais de pontuação, "
            "97 são letras maiúsculas, e 94 são caracteres especiais.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    small_site_one_url = [
        pytest.param(
            "en",
            "There is a total of 501 characters. Of these, 115 are punctuation marks, "
            "107 are uppercase letters, and 76 are special characters.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Há um total de caracteres 501. Destes, 115 são sinais de pontuação, "
            "107 são letras maiúsculas, e 76 são caracteres especiais.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    big_site_one_url = [
        pytest.param(
            "en",
            "There is a total of 100001 characters. Of these, "
            "24506 are punctuation marks, 19775 are uppercase letters, "
            "and 17474 are special characters.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Há um total de caracteres 100001. Destes, "
            "24506 são sinais de pontuação, 19775 são letras maiúsculas, "
            "e 17474 são caracteres especiais.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    small_site_four_url = [
        pytest.param(
            "en",
            "There is a total of 2004 characters. Of these, 460 are punctuation marks, "
            "428 are uppercase letters, and 304 are special characters.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Há um total de caracteres 2004. Destes, 460 são sinais de pontuação, "
            "428 são letras maiúsculas, e 304 são caracteres especiais.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]
