from typing import ClassVar

import pytest


class Params:
    decorators: ClassVar[list] = [
        pytest.param(
            "en",
            "Save or remove a custom color.",
            "Usage: +set color (#hex or remove)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Salvar ou remover uma cor personalizada.",
            "Uso: +set color (#hex ou remove)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    color_set: ClassVar[list] = [
        pytest.param(
            "en",
            "#000000",
            "Saved color changed successfully.",
            marks=pytest.mark.en,
            id="set-en",
        ),
        pytest.param(
            "pt_BR",
            "#ffffff",
            "Cor salva alterada com sucesso.",
            marks=pytest.mark.pt_BR,
            id="set-pt",
        ),
    ]

    color_set_no_hash: ClassVar[list] = [
        pytest.param(
            "en",
            "123abc",
            "Saved color changed successfully.",
            marks=pytest.mark.en,
            id="set-nohash-en",
        ),
        pytest.param(
            "pt_BR",
            "abc123",
            "Cor salva alterada com sucesso.",
            marks=pytest.mark.pt_BR,
            id="set-nohash-pt",
        ),
    ]

    color_set_short_hex: ClassVar[list] = [
        pytest.param(
            "en",
            "#fff",
            "Saved color changed successfully.",
            marks=pytest.mark.en,
            id="short-en",
        ),
        pytest.param(
            "pt_BR",
            "abc",
            "Cor salva alterada com sucesso.",
            marks=pytest.mark.pt_BR,
            id="short-pt",
        ),
    ]

    color_remove: ClassVar[list] = [
        pytest.param(
            "en",
            "remove",
            "Saved color removed successfully.",
            marks=pytest.mark.en,
            id="remove-en",
        ),
        pytest.param(
            "pt_BR",
            "remove",
            "Cor salva removida com sucesso.",
            marks=pytest.mark.pt_BR,
            id="remove-pt",
        ),
    ]

    color_invalid: ClassVar[list] = [
        pytest.param(
            "en",
            "this-is-not-a-color",
            "Saved color changed successfully.",
            marks=pytest.mark.en,
            id="invalid-en",
        ),
        pytest.param(
            "pt_BR",
            "semcorvalida",
            "Cor salva alterada com sucesso.",
            marks=pytest.mark.pt_BR,
            id="invalid-pt",
        ),
    ]
