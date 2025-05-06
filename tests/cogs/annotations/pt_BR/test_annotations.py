# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.annotations.command.annotations import AnnotationsCmd
from tests.cogs.annotations.templates import templates
from tests.helpers.mock_classes import MockContext

lang = "pt_BR"


@pytest_asyncio.fixture
async def interact(mock_bot):
    return AnnotationsCmd(bot=mock_bot)


@pytest.mark.asyncio
async def test_annotations(interact, mock_context: MockContext):
    expected = ["", 1, "Shush"]
    await templates.test_annotations(interact, mock_context, lang=lang, content="", expected=expected)


@pytest.mark.asyncio
async def test_annotations_add_no_content(interact, mock_context: MockContext):
    await templates.test_annotations_add(
        interact, mock_context, lang=lang, content="", expected="Você precisa fornecer conteúdo para este comando."
    )


@pytest.mark.asyncio
async def test_annotations_add_content_no_title(interact, mock_context: MockContext):
    await templates.test_annotations_add(
        interact,
        mock_context,
        lang=lang,
        content="A note about something I want to be able to check forever.",
        expected="Nota criada com sucesso. 📝 (ID: 1)",
    )


@pytest.mark.asyncio
async def test_annotations_add_content_too_long_no_title(interact, mock_context: MockContext):
    await templates.test_annotations_add(
        interact, mock_context, lang=lang, content="a" * 451, expected="A mensagem deve ter no máximo 450 caracteres."
    )


@pytest.mark.asyncio
async def test_annotations_add_content_title(interact, mock_context: MockContext):
    await templates.test_annotations_add(
        interact,
        mock_context,
        lang=lang,
        content='title:"title easier to remember" A note about something I want to be able to check forever.',
        expected="Nota criada com sucesso. 📝 (ID: 1)",
    )


@pytest.mark.asyncio
async def test_annotations_add_content_title_too_long(interact, mock_context: MockContext):
    await templates.test_annotations_add(
        interact,
        mock_context,
        lang=lang,
        content='title:"title to make it easier to remember the content" '
        "A note about something I want to be able to check forever.",
        expected="O título deve ter um máximo de 32 caracteres.",
    )


@pytest.mark.asyncio
async def test_annotations_check_wrong_id(interact, mock_context: MockContext):
    await templates.test_annotations_check(
        interact, mock_context, lang=lang, content="title", expected="title não é um ID valido."
    )


@pytest.mark.asyncio
async def test_annotations_check_no_content_no_annotations(interact, mock_context: MockContext):
    await templates.test_annotations_check(
        interact, mock_context, lang=lang, content="", expected="Você não tem nenhuma anotação salva."
    )


@pytest.mark.asyncio
async def test_annotations_check_one_annotation(interact, mock_context: MockContext):
    await templates.test_annotations_check(
        interact,
        mock_context,
        lang=lang,
        content="",
        expected="Suas anotações são aquelas com ID: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa [1]",
        amount=1,
    )


@pytest.mark.asyncio
async def test_annotations_check_two_annotation(interact, mock_context: MockContext):
    await templates.test_annotations_check(
        interact,
        mock_context,
        lang=lang,
        content="",
        expected="Suas anotações são aquelas com ID: "
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa [1], "
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa [2]",
        amount=2,
    )


@pytest.mark.asyncio
async def test_annotations_check_annotation_id_one(interact, mock_context: MockContext):
    await templates.test_annotations_check(
        interact,
        mock_context,
        lang=lang,
        content="1",
        expected="a note about something I want to be able to check forever. 0",
        amount=2,
    )


@pytest.mark.asyncio
async def test_annotations_check_annotation_id_two(interact, mock_context: MockContext):
    await templates.test_annotations_check(
        interact,
        mock_context,
        lang=lang,
        content="2",
        expected="a note about something I want to be able to check forever. 1",
        amount=2,
    )


@pytest.mark.asyncio
async def test_annotations_check_annotation_wrong_id(interact, mock_context: MockContext):
    await templates.test_annotations_check(
        interact, mock_context, lang=lang, content="3", expected="Você não tem nenhuma anotação com ID 3.", amount=2
    )


@pytest.mark.asyncio
async def test_annotations_delete_no_id(interact, mock_context: MockContext):
    await templates.test_annotations_delete(
        interact, mock_context, lang=lang, content="", expected="Você precisa fornecer um ID numérico válido.", amount=2
    )


@pytest.mark.asyncio
async def test_annotations_delete_id(interact, mock_context: MockContext):
    await templates.test_annotations_delete(
        interact,
        mock_context,
        lang=lang,
        content="1",
        expected="Sua anotação com ID 1 foi excluída com sucesso. 🗑",
        amount=2,
    )
