# -*- coding: utf-8 -*-

import pytest


class Params:
    decorators = [
        pytest.param(
            "en",
            "This subcommand is used to add an alias.",
            "How to use: {}alias add (name) (command) (…arguments)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Este subcomando é usado para adicionar um alias.",
            "Como usar: {}alias add (nome) (comando) (…argumentos)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    no_content = [
        pytest.param(
            "en",
            "You didn't send a command! Usage: +alias add (name) (command) (…arguments)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Você não enviou um comando! Use: +alias add (nome) (comando) (…argumentos)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    invalid_name = [
        pytest.param(
            "en",
            "Your alias name is not valid! Your alias should only contain letters, "
            "numbers and be 2-30 characters long.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Seu nome de alias não é válido! Seu alias deve conter apenas letras, "
            "números e ter entre 2-30 caracteres de comprimento.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    valid_name = [
        pytest.param("en", 'Your alias "{name}" has been created successfully.', marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", 'Seu alias "{name}" foi criado com sucesso.', marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    conflict = [
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

    guard_caught = [
        pytest.param(
            "en",
            'You are not authorized to use the "restart" command due to "DevRequired". '
            "If you think this is an error, contact @dev_name.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            'Você não está autorizado a usar o comando "restart" motivo: '
            '"DevRequired". Se achar que isso é um erro, entre em contato com @dev_name.',
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    success = [
        pytest.param("en", 'Your alias "The_Tests" has been created successfully.', marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", 'Seu alias "The_Tests" foi criado com sucesso.', marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    pipe_guard_caught = [
        pytest.param(
            "en",
            'You are not authorized to use the "restart" command due to "DevRequired". '
            "If you think this is an error, contact @dev_name.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            'Você não está autorizado a usar o comando "restart" motivo: "DevRequired". '
            "Se achar que isso é um erro, entre em contato com @dev_name.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    pipe_success = [
        pytest.param("en", 'Your alias "advanced_usage" has been created successfully.', marks=pytest.mark.en, id="en"),
        pytest.param(
            "pt_BR", 'Seu alias "advanced_usage" foi criado com sucesso.', marks=pytest.mark.pt_BR, id="pt_BR"
        ),
    ]
