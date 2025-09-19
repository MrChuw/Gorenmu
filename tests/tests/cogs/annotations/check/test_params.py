# -*- coding: utf-8 -*-

import pytest


class Params:
    decorators = [
        pytest.param(
            "en",
            "This subcommand is used to check infos for an note.",
            "How to use: +note check (id)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Este subcomando é usado para verificar uma anotação.",
            "Como usar: +note check (id)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
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
