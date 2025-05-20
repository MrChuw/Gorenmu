# -*- coding: utf-8 -*-

import pytest


class Params:
    annotations = [
        pytest.param("en", ["", 1, "Shush"], marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", ["", 1, "Shush"], marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    add_no_content = [
        pytest.param("en", "You need to provide content for this command.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "Você precisa fornecer conteúdo para este comando.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    add_content_no_title = [
        pytest.param("en", "Note successfully created. 📝 (ID: 1)", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "Nota criada com sucesso. 📝 (ID: 1)", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    add_content_too_long_no_title = [
        pytest.param("en", "The message must have a maximum of 450 characters.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "A mensagem deve ter no máximo 450 caracteres.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    add_content_title = [
        pytest.param("en", "Note successfully created. 📝 (ID: 1)", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "Nota criada com sucesso. 📝 (ID: 1)", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    add_content_title_too_long = [
        pytest.param("en", "The title must have a maximum of 32 characters.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "O título deve ter um máximo de 32 caracteres.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    check_wrong_id = [
        pytest.param("en", "title is not a valid ID.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "title não é um ID valido.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    check_no_content_no_annotations = [
        pytest.param("en", "You don't have any annotations saved.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "Você não tem nenhuma anotação salva.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    check_one_annotation = [
        pytest.param(
            "en",
            "Your annotations are the ones with ID: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa [1]",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Suas anotações são aquelas com ID: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa [1]",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    check_two_annotation = [
        pytest.param(
            "en",
            "Your annotations are the ones with ID: "
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa [1], "
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa [2]",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Suas anotações são aquelas com ID: "
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa [1], "
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa [2]",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    check_annotation_id_one = [
        pytest.param(
            "en", "a note about something I want to be able to check forever. 0", marks=pytest.mark.en, id="en"
        ),
        pytest.param(
            "pt_BR", "a note about something I want to be able to check forever. 0", marks=pytest.mark.pt_BR, id="pt_BR"
        ),
    ]

    check_annotation_id_two = [
        pytest.param(
            "en", "a note about something I want to be able to check forever. 1", marks=pytest.mark.en, id="en"
        ),
        pytest.param(
            "pt_BR", "a note about something I want to be able to check forever. 1", marks=pytest.mark.pt_BR, id="pt_BR"
        ),
    ]

    check_annotation_wrong_id = [
        pytest.param("en", "You don't have any annotation with ID 3.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "Você não tem nenhuma anotação com ID 3.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    delete_no_id = [
        pytest.param("en", "You need to provide a valid numeric ID.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "Você precisa fornecer um ID numérico válido.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    delete_id = [
        pytest.param("en", "Your annotation with ID 1 was successfully deleted. 🗑", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "Sua anotação com ID 1 foi excluída com sucesso. 🗑", marks=pytest.mark.pt_BR, id="pt_BR")
    ]
