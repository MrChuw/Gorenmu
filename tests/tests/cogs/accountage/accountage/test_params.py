import datetime
from typing import ClassVar

import pytest


class Params:
    _created_at = datetime.datetime(2019, 1, 20, 19, 34, 45, tzinfo=datetime.UTC)

    decorators: ClassVar[list] = [
        pytest.param(
            "en",
            "Check the Twitch account creation date.",
            "Usage: +accountage (username)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Verifica a data de criação de uma conta da Twitch.",
            "Uso: +accountage (nome_de_usuário)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    yourself: ClassVar[list] = [
        pytest.param(
            "en",
            'you created the account on 01/20/2019 at 07:34 PM '
            '(6 years, 6 months, 18 days, 21 hours, 31 minutes and 10 seconds ago)',
            marks=pytest.mark.en,
            id="yourself-en",
        ),
        pytest.param(
            "pt_BR",
            'você criou a conta em 20/01/2019 às 19:34:45 '
            '(há 6 anos, 6 meses, 18 dias, 21 horas, 31 minutos e 10 segundos)',
            marks=pytest.mark.pt_BR,
            id="yourself-pt",
        ),
    ]

    other: ClassVar[list] = [
        pytest.param(
            "en",
            '@mr_chuw created the account on 01/20/2019 at 07:34 PM '
            '(6 years, 6 months, 18 days, 21 hours, 31 minutes and 10 seconds ago)',
            marks=pytest.mark.en,
            id="other-en",
        ),
        pytest.param(
            "pt_BR",
            '@mr_chuw criou a conta em 20/01/2019 às 19:34:45 '
            '(há 6 anos, 6 meses, 18 dias, 21 horas, 31 minutos e 10 segundos)',
            marks=pytest.mark.pt_BR,
            id="other-pt",
        ),
    ]

    not_found: ClassVar[list] = [
        pytest.param(
            "en",
            "I couldn't find any user named @asdfasdf.",
            marks=pytest.mark.en,
            id="notfound-en",
        ),
        pytest.param(
            "pt_BR",
            "Não consegui encontrar nenhum usuário chamado @asdfasdf.",
            marks=pytest.mark.pt_BR,
            id="notfound-pt",
        ),
    ]
