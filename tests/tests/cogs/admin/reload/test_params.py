# -*- coding: utf-8 -*-

import pytest


class Params:
    translations = [
        pytest.param("en", "The translations were successfully reloaded.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "As traduções foram recarregadas com sucesso.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    emotes = [
        pytest.param("en", "The emotes were successfully reloaded.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "Os emotes foram recarregadas com sucesso.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    commands = [
        pytest.param("en", "The commands were successfully reloaded.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "Os comandos foram recarregados com sucesso.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    all = [
        pytest.param(
            "en",
            "The translations were successfully reloaded. "
            "The emotes were successfully reloaded. "
            "The commands were successfully reloaded.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "As traduções foram recarregadas com sucesso. "
            "Os emotes foram recarregadas com sucesso. "
            "Os comandos foram recarregados com sucesso.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    error_translations = [
        pytest.param("en", "The translations had an error while reloading: Error", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "As traduções tiveram um erro ao recarregar: Error", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    error_emotes = [
        pytest.param("en", "The emotes had an error while reloading: Error", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "Os emotes tiveram um erro ao recarregar: Error", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]
