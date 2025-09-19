# -*- coding: utf-8 -*-

import pytest


class Params:
    decorators = [
        pytest.param("en", "Get your daily fortune.", "To use: +cookie eat", marks=pytest.mark.en, id="en"),
        pytest.param(
            "pt_BR",
            "Pegue seu biscoito da sorte diário.",
            "Para usar: +cookie eat",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    with_nothing = [
        pytest.param(
            "en",
            ["The person born with a talent they are meant to use will find their greatest happiness in using it."],
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param("pt_BR", ["Porque ser contra o que é felicidade é loucura."], marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    amount_zero = [
        pytest.param("en", ["You didn't eat anything, wow!"], marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", ["Você não comeu nada, nossa!"], marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    amount_negative = [
        pytest.param(
            "en", ["To eat -1 cookies, you must first know how to reverse entropy."], marks=pytest.mark.en, id="en"
        ),
        pytest.param(
            "pt_BR",
            ["Para comer -1 cookies, você deve primeiro saber como reverter entropia."],
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    multiple_amount = [
        pytest.param("en", ["you ate 2 cookies in one sitting. 🥠"], marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", ["você comeu 2 cookies de uma só vez. 🥠"], marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    cooldown = [
        pytest.param(
            "en",
            [
                "The person born with a talent they are meant to use will find their greatest happiness in using it.",
                "The trouble with most people is that they think with "
                "their hopes or fears or wishes rather than with their minds.",
                "You're still on cooldown, wait 5 hours, 59 minutes and",
            ],
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            [
                "Porque ser contra o que é felicidade é loucura.",
                "Se a vida te afastar, lute por cada centímetro.",
                "Você ainda está em cooldown, espere 5 horas, 59 minutos e",
            ],
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]
