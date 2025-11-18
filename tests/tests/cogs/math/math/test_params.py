# -*- coding: utf-8 -*-

import pytest


class Params:
    decorators = [
        pytest.param(
            "en",
            "Enter the command and a mathematical operation for me to solve it.",
            "To use: +math (mathematical expression)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Digite o comando e uma operação matemática para eu resolvê-la.",
            "Para usar: +math (expressão matemática)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    simple_formula = [
        pytest.param("en", "2", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "2", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    not_so_simple_formula = [
        pytest.param("en", "723.4998272287285", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "723.4998272287285", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    multi_line_ish_formula = [
        pytest.param("en", "[[0, 6]]", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "[[0, 6]]", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    error = [
        pytest.param(
            "en",
            "An unexpected error occurred. Please report it to @dev_name on whispers.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Ocorreu um erro inesperado. Por favor, reporte-o para @dev_name nos whispers.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]
