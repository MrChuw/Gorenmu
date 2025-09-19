# -*- coding: utf-8 -*-
import pytest


class Params:
    decorators = [
        pytest.param(
            "en", "Enable or disable bot mentions.", "Usage: +set mention <on/off>", marks=pytest.mark.en, id="en"
        ),
        pytest.param(
            "pt_BR",
            "Ativar ou desativar menções do bot.",
            "Uso: +set mention <on/off>",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    valid_on = [
        pytest.param(
            "en",
            "on",
            "You will start receiving pings from the bot on commands again.",
            marks=pytest.mark.en,
            id="on-en",
        ),
        pytest.param(
            "pt_BR", "on", "Você voltará a receber menções do bot nos comandos.", marks=pytest.mark.pt_BR, id="on-pt"
        ),
    ]

    valid_off = [
        pytest.param(
            "en",
            "off",
            "Every time the bot says your nick it will place an invisible character to prevent ping.",
            marks=pytest.mark.en,
            id="off-en",
        ),
        pytest.param(
            "pt_BR",
            "off",
            "Sempre que o bot disser seu nick, ele colocará um caractere invisível para evitar o ping.",
            marks=pytest.mark.pt_BR,
            id="off-pt",
        ),
    ]

    invalid_input = [
        pytest.param(
            "en",
            "maybe",
            'maybe its not a valid option, choose between "on" or "off"',
            marks=pytest.mark.en,
            id="invalid-en",
        ),
        pytest.param(
            "pt_BR",
            "talvez",
            'talvez não é uma opção válida, escolha entre "on" ou "off"',
            marks=pytest.mark.pt_BR,
            id="invalid-pt",
        ),
    ]
