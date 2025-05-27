# -*- coding: utf-8 -*-

import pytest


class Params:
    on_cooldown = [
        pytest.param(
            "en",
            r"You're still on cooldown, wait \d+\.\d{2} seconds until the next batch! ⌛",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            r"Você ainda está em cooldown, espere \d+\.\d{2} segundos até o próximo lote! ⌛",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    no_content = [
        pytest.param("en", "you stocked 1 cookies 🍪.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "você estocou 1 cookies 🍪.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    all = [
        pytest.param("en", "you stocked 4 cookies 🍪, the next one comes out in 6h.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "você estocou 4 cookies 🍪, o próximo sai em 6h.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    with_amount = [
        pytest.param("en", "you stocked 1 cookies 🍪.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "você estocou 1 cookies 🍪.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    with_exact_amount = [
        pytest.param("en", "you stocked 4 cookies 🍪, the next one comes out in 6h.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "você estocou 4 cookies 🍪, o próximo sai em 6h.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    not_enough_cookies = [
        pytest.param("en", "you can only stock 4 🍪.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "você só pode estocar 4.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]
