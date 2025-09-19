# -*- coding: utf-8 -*-
import pytest


class Params:
    decorators = [
        pytest.param("en", "Return to AFK status.", "To use: +rafk", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "Retornar ao status AFK.", "Para usar: +rafk", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    not_in_time = [
        pytest.param("en", "Time to return AFK has already expired.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "O tempo para retornar AFK já expirou.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    with_content = [
        pytest.param("en", "you continued afk 🏃⌨ and left a note with: content", marks=pytest.mark.en, id="en"),
        pytest.param(
            "pt_BR", "você continuou ausente 🏃⌨ e deixou uma nota com: content", marks=pytest.mark.pt_BR, id="pt_BR"
        ),
    ]

    no_content = [
        pytest.param("en", "you continued afk 🏃⌨", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "você continuou ausente 🏃⌨", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]
