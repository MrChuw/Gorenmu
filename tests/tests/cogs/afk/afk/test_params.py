# -*- coding: utf-8 -*-
import pytest


class Params:
    no_content = [
        pytest.param("en", "you went afk 🏃⌨", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "você ficou ausente 🏃⌨", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    content = [
        pytest.param("en", "you went afk 🏃⌨ and left a note with: Just a test", marks=pytest.mark.en, id="en"),
        pytest.param(
            "pt_BR", "você ficou ausente 🏃⌨ e deixou uma nota com: Just a test", marks=pytest.mark.pt_BR, id="pt_BR"
        ),
    ]

    too_much_content = [
        pytest.param("en", "The message must have a maximum of 450 characters.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "A mensagem deve ter no máximo 450 caracteres.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]
