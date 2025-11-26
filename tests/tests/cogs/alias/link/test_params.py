from typing import ClassVar

import pytest


class Params:
    decorators: ClassVar[list] = [
        pytest.param(
            "en",
            "This subcommand is used to create link for an alias.",
            "How to use: +alias link (user) cool_name",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Este subcomando é usado para criar um link para um alias.",
            "Como usar: +alias link (usuário) cool_name",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    no_content: ClassVar[list] = [
        pytest.param(
            "en",
            "You didn't provide a user or alias name! Use: +alias link (user) (alias name)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Você não forneceu um nome de usuário ou alias! Use: +alias link (usuário) (nome do alias)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    alias_conflict: ClassVar[list] = [
        pytest.param(
            "en",
            'Cannot add alias "The_Tests_alias" - you already have one! '
            'You can either "edit" its definition, "rename" it or "remove" it.',
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            'Não é possível adicionar o alias "The_Tests_alias" - você já possui um! '
            "Você pode “editar” sua definição, “renomear” ou “removê-la”.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    name_conflict: ClassVar[list] = [
        pytest.param(
            "en",
            "Cannot link a new alias - you already have an alias named: The_Tests_alias!",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Não é possível vincular um novo alias - você já possui um alias nomeado: The_Tests_alias!",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    wrong_username: ClassVar[list] = [
        pytest.param(
            "en",
            "I couldn't find any user named @Wrong_username.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Não consegui encontrar nenhum usuário chamado @Wrong_username.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    user_no_alias: ClassVar[list] = [
        pytest.param(
            "en",
            'The provided user does not have the alias "The_Alias_"!',
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            'O usuário fornecido não possui o alias "The_Alias_"!',
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    user_link_to_link: ClassVar[list] = [
        pytest.param(
            "en",
            "You tried to create a link from a linked alias "
            "(alias The_Alias_link_link by The_Tests_user), "
            "so I used the original as your template. When the original changes, yours will too.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Você tentou criar um link a partir de um alias link "
            "(alias The_Alias_link_link por The_Tests_user), "
            "então usei o original como modelo. Quando o original mudar, o seu também mudará.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    user_link_to_link_custom_name: ClassVar[list] = [
        pytest.param(
            "en",
            "You tried to create a link from a linked alias "
            "(alias The_Alias_link_link by The_Tests_user), "
            'so I used the original as your template, with a custom name of "Custom_Name". '
            "When the original changes, yours will too.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Você tentou criar um link a partir de um alias link "
            "(alias The_Alias_link_link por The_Tests_user), então usei o original como modelo, "
            'com um nome personalizado de "Custom_Name". Quando o original mudar, o seu também mudará.',
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    user_alias_success: ClassVar[list] = [
        pytest.param(
            "en",
            "Alias successfully linked. When the original changes, yours will too.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Alias vinculado com sucesso. Quando o original for alterado, o seu também será.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    user_alias_custom_name_success: ClassVar[list] = [
        pytest.param(
            "en",
            'Alias successfully linked, with a custom name of "Custom_Name". '
            "When the original changes, yours will too.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            'Alias vinculado com sucesso, com um nome personalizado de "Custom_Name". '
            "Quando o original for alterado, o seu também será.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]
