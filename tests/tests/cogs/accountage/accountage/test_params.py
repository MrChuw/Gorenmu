# -*- coding: utf-8 -*-

import datetime

import pytest


class Params:
    _created_at = datetime.datetime(2019, 1, 20, 19, 34, 45, tzinfo=datetime.UTC)

    decorators = [
        pytest.param(
            "en",
            "Check the Twitch account creation date.",
            "Usage: {}accountage (username)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Verifica a data de criação de uma conta da Twitch.",
            "Uso: {}accountage (nome_de_usuário)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    yourself = [
        pytest.param(
            "en",
            r"you created the account on \d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2} "
            r"\(\d+ years, \d+ months, \d+ days, \d+ hours, \d+ minutes and \d+\.\d+ seconds ago\)",
            marks=pytest.mark.en,
            id="yourself-en",
        ),
        pytest.param(
            "pt_BR",
            r"você criou a conta em \d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2} "
            r"\(há \d+ anos, \d+ meses, \d+ dias, \d+ horas, \d+ minutos e \d+\.\d+ segundos\)",
            marks=pytest.mark.pt_BR,
            id="yourself-pt",
        ),
    ]

    other = [
        pytest.param(
            "en",
            r"@mr_chuw created the account on \d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2} "
            r"\(\d+ years, \d+ months, \d+ days, \d+ hours, \d+ minutes and \d+\.\d+ seconds ago\)",
            marks=pytest.mark.en,
            id="other-en",
        ),
        pytest.param(
            "pt_BR",
            r"@mr_chuw criou a conta em \d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2} "
            r"\(há \d+ anos, \d+ meses, \d+ dias, \d+ horas, \d+ minutos e \d+\.\d+ segundos\)",
            marks=pytest.mark.pt_BR,
            id="other-pt",
        ),
    ]

    not_found = [
        pytest.param("en", "I couldn't find any user named @asdfasdf.", marks=pytest.mark.en, id="notfound-en"),
        pytest.param(
            "pt_BR",
            "Não consegui encontrar nenhum usuário chamado @asdfasdf.",
            marks=pytest.mark.pt_BR,
            id="notfound-pt",
        ),
    ]
