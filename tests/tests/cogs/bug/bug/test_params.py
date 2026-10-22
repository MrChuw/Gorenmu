from typing import ClassVar

import pytest


class Params:
    decorators: ClassVar[list] = [
        pytest.param(
            "en",
            "report a bug that occurred in the Bot.",
            "To use: +bug (description)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "reporte um bug que ocorreu no Bot.",
            "Para usar: +bug (descrição)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    no_content: ClassVar[list] = [
        pytest.param("en", 'your bug has been reported 🐛 (ID 1)', marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", 'seu bug foi reportado 🐛 (ID 1)', marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    params_: ClassVar[list] = [
        pytest.param("en", "blablabla", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "blablabla", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]
