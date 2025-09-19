# -*- coding: utf-8 -*-

import pytest


class Params:
    decorators = [
        pytest.param(
            "en",
            "Set or remove your saved city.",
            "Usage: +set city (name or remove) [hidden:true]",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Definir ou remover sua cidade salva.",
            "Uso: +set city (nome ou remove) [hidden:true]",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    set_city_add = [
        pytest.param("en", "New York", "City added successfully.", marks=pytest.mark.en, id="add-en"),
        pytest.param("pt_BR", "São Paulo", "Cidade adicionada com sucesso.", marks=pytest.mark.pt_BR, id="add-pt"),
    ]

    set_city_add_hidden = [
        pytest.param("en", "Tokyo hidden:true", "City added successfully.", marks=pytest.mark.en, id="hidden-en"),
        pytest.param(
            "pt_BR", "Recife hidden:true", "Cidade adicionada com sucesso.", marks=pytest.mark.pt_BR, id="hidden-pt"
        ),
    ]

    set_city_remove = [
        pytest.param("en", "remove", "City removed successfully.", marks=pytest.mark.en, id="remove-en"),
        pytest.param("pt_BR", "remove", "Cidade removida com sucesso.", marks=pytest.mark.pt_BR, id="remove-pt"),
    ]
