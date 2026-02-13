from typing import ClassVar

import pytest


class Params:
    decorators: ClassVar[list] = [
        pytest.param(
            "en",
            "Command used to manage cookies.",
            "To use: +cookie Eat|Count|Gift|Stock|Top|SlotMachine (options)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Comando usado para gerenciar cookies.",
            "Para usar: +cookie Eat|Count|Gift|Stock|Top|SlotMachine (opções)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    cookie: ClassVar[list] = [
        pytest.param(
            "en",
            'Choose from one of the options "eat", "count", "top", "gift", "stock" or "sm"',
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            'Escolha entre uma das opções "eat", "count", "top", "gift", "stock" ou "sm"',
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]
