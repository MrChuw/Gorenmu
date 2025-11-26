from typing import ClassVar

import pytest


class Params:
    decorators: ClassVar[list] = [
        pytest.param(
            "en",
            "Reloads the commands using all or command name.",
            "How to use: +reload (all) or (command_name)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Recarregar os comandos usando all ou nome do comando.",
            "Como usar: +reload (all) ou (command_name)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    translations: ClassVar[list] = [
        pytest.param(
            "en",
            "Translations were successfully reloaded.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Translations foram recarregadas com sucesso.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    emotes: ClassVar[list] = [
        pytest.param("en", "Emotes were successfully reloaded.", marks=pytest.mark.en, id="en"),
        pytest.param(
            "pt_BR",
            "Emotes foram recarregadas com sucesso.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    commands: ClassVar[list] = [
        pytest.param(
            "en",
            "The commands were successfully reloaded.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Os comandos foram recarregados com sucesso.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    all: ClassVar[list] = [
        pytest.param(
            "en",
            "The commands were successfully reloaded. ",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Os comandos foram recarregados com sucesso.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    error_translations: ClassVar[list] = [
        pytest.param(
            "en",
            "Translations had an error while reloading: Error",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Translations tiveram um erro ao recarregar: Error",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    error_emotes: ClassVar[list] = [
        pytest.param(
            "en",
            "Emotes had an error while reloading: Error",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Emotes tiveram um erro ao recarregar: Error",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]
