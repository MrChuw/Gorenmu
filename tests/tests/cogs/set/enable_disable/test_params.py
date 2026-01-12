from typing import ClassVar

import pytest


class Params:
    decorators: ClassVar[list] = [
        pytest.param(
            "en",
            "A command used to activate or deactivate other commands.",
            "To use: +set enable/disable (command name or all)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Um comando usado para ativar ou desativar outros comandos.",
            "Para usar: +set enable/disable (nome do comando or all)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    enable: ClassVar[list] = [
        pytest.param("en", "The command wt was activated.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "O comando wt foi ativado.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    enable_all: ClassVar[list] = [
        pytest.param("en", "All commands have been activated.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "Todos os comandos foram ativados.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    disable: ClassVar[list] = [
        pytest.param("en", "The command wt was disabled.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "O comando wt foi desativado.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    disable_all: ClassVar[list] = [
        pytest.param("en", "All commands have been disabled.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "Todos os comandos foram desativados.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]
