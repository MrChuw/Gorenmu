from typing import ClassVar

import pytest


class Params:
    decorators: ClassVar[list] = [
        pytest.param(
            "en",
            "Enable or disable reminders.",
            "Usage: +set reminder (on/off)",
            marks=pytest.mark.en,
            id="decorator-en",
        ),
        pytest.param(
            "pt_BR",
            "Ativar ou desativar lembretes.",
            "Uso: +set reminder (on/off)",
            marks=pytest.mark.pt_BR,
            id="decorator-pt",
        ),
    ]

    enable: ClassVar[list] = [
        pytest.param(
            "en",
            "on",
            "Reminder successfully turned on.",
            marks=pytest.mark.en,
            id="on-en",
        ),
        pytest.param(
            "pt_BR",
            "on",
            "Lembrete ativado com sucesso.",
            marks=pytest.mark.pt_BR,
            id="on-pt",
        ),
    ]

    disable: ClassVar[list] = [
        pytest.param(
            "en",
            "off",
            "Reminder successfully turned off.",
            marks=pytest.mark.en,
            id="off-en",
        ),
        pytest.param(
            "pt_BR",
            "off",
            "Lembrete desativado com sucesso.",
            marks=pytest.mark.pt_BR,
            id="off-pt",
        ),
    ]

    invalid: ClassVar[list] = [
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
