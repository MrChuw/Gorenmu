# -*- coding: utf-8 -*-

import pytest


class Params:
    decorators = [
        pytest.param(
            "en",
            "This subcommand is used to copy an alias.",
            "How to use: {}alias copy (user) (alias) (…arguments)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Este subcomando é usado para copiar um alias.",
            "Como usar: {}alias copy (usuário) (alias) (…argumentos)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    no_content = [
        pytest.param("en", "No target user provided!", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "Nenhum usuário alvo fornecido!", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    user_no_alias = [
        pytest.param("en", "No target alias provided!", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "Nenhum alias de destino fornecido!", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    user_invalid_alias = [
        pytest.param(
            "en", "The copied alias's name is not valid and therefore can't be copied!", marks=pytest.mark.en, id="en"
        ),
        pytest.param(
            "pt_BR",
            "O nome do alias copiado não é válido e portanto não pode ser copiado!",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    user_alias_conflict = [
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

    user_not_found = [
        pytest.param("en", "I couldn't find any user named @The_Tests_ser.", marks=pytest.mark.en, id="en"),
        pytest.param(
            "pt_BR",
            "Não consegui encontrar nenhum usuário chamado @The_Tests_ser.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    user_alias_not_found = [
        pytest.param("en", "I couldn't find Invalid_alias in user The_Tests_user!", marks=pytest.mark.en, id="en"),
        pytest.param(
            "pt_BR",
            "Não consegui encontrar Invalid_alias no usuário The_Tests_user!",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    user_alias_link = [
        pytest.param(
            "en",
            "You cannot copy links to other aliases. Instead, use +alias copy The_Tests_user The_Alias_test",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Você não pode copiar links para outros aliases. "
            "Em vez disso, use +alias copy The_Tests_user The_Alias_test",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    user_alias_success = [
        pytest.param("en", 'Alias "The_Alias_test" copied successfully.', marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", 'Alias "The_Alias_test" copiado com sucesso.', marks=pytest.mark.pt_BR, id="pt_BR"),
    ]
