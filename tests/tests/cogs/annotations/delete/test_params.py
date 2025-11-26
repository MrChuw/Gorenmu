from typing import ClassVar

import pytest


class Params:
    decorators: ClassVar[list] = [
        pytest.param(
            "en",
            "This subcommand is used to delete an note.",
            "How to use: +note delete cool_name",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Este subcomando é usado para deletar uma anotação.",
            "Como usar: +note delete (id)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    delete_no_id: ClassVar[list] = [
        pytest.param(
            "en",
            "You need to provide a valid numeric ID.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Você precisa fornecer um ID numérico válido.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    delete_id: ClassVar[list] = [
        pytest.param(
            "en",
            "Your annotation with ID 1 was successfully deleted. 🗑",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Sua anotação com ID 1 foi excluída com sucesso. 🗑",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]
