from typing import ClassVar

import pytest


class Params:
    decorators: ClassVar[list] = [
        pytest.param(
            "en",
            "This subcommand is used to edit the command and arguments for an alias.",
            "How to use: +alias edit (alias) (command) (…arguments)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Este subcomando é usado para editar o comando e os argumentos de um alias.",
            "Como usar: +alias edit (alias) (comando) (…argumentos)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    no_content: ClassVar[list] = [
        pytest.param("en", "No alias or command name provided!", marks=pytest.mark.en, id="en"),
        pytest.param(
            "pt_BR",
            "Nenhum alias ou nome de comando fornecido!",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    wrong_name_no_command: ClassVar[list] = [
        pytest.param("en", "No alias or command name provided!", marks=pytest.mark.en, id="en"),
        pytest.param(
            "pt_BR",
            "Nenhum alias ou nome de comando fornecido!",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    wrong_name_wrong_command: ClassVar[list] = [
        pytest.param(
            "en",
            'You don\'t have the "Wrong_alias" alias!',
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            'Você não tem o alias "Wrong_alias"!',
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    name_wrong_command: ClassVar[list] = [
        pytest.param(
            "en",
            'Cannot edit alias! The command "blablablablablablablablablablablabla" does not exist.',
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            'Não é possível editar o alias! O comando "blablablablablablablablablablablabla" não existe.',
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    alias_link_wrong_command: ClassVar[list] = [
        pytest.param(
            "en",
            "You cannot edit links to other aliases!",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Você não pode editar links para outros aliases!",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    guard_caught: ClassVar[list] = [
        pytest.param(
            "en",
            'You are not authorized to use the "restart" command due to "DevRequiredError". '
            "If you think this is an error, contact @dev_name.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            'Você não está autorizado a usar o comando "restart" motivo: "DevRequiredError". '
            "Se achar que isso é um erro, entre em contato com @dev_name.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    describe_success: ClassVar[list] = [
        pytest.param(
            "en",
            'Your alias "The_Tests_alias" has been successfully edited.',
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            'Seu alias "The_Tests_alias" foi editado com sucesso.',
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]
