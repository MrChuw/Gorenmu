# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.annotations.command.annotations import AnnotationsCmd
from bot.models import Annotation
from bot.translations import Response
from tests.helpers.mock_classes import MockContext


@pytest_asyncio.fixture
async def interact(mock_bot):
    return AnnotationsCmd(bot=mock_bot)


@pytest.fixture
def mock_context(mock_bot):
    return MockContext("username", 12345, "channelname", 123456, mock_bot)


@pytest.mark.asyncio
async def test_annotations(interact, mock_context: MockContext):
    await mock_context.prepare_context('pt_BR')
    response: Response = await interact.annotations._callback(self=interact, ctx=mock_context)
    assert response.response_string == ""
    assert mock_context.simple_response.call_count == 1
    assert mock_context.simple_response.call_args_list[0][0][1] == "Shush"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_annotations_add_no_content(interact, mock_context: MockContext):
    await mock_context.prepare_context('pt_BR')
    response: Response = await interact.add._callback(self=interact, ctx=mock_context, content="")
    assert response.response_string == 'Você precisa fornecer conteúdo para este comando.'
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_annotations_add_content_no_title(interact, mock_context: MockContext):
    await mock_context.prepare_context('pt_BR')
    response: Response = await interact.add._callback(
            self=interact,
            ctx=mock_context,
            content="A note about something I want to be able to check forever."
    )
    assert response.response_string == 'Nota criada com sucesso. 📝 (ID: 1)'
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_annotations_add_content_too_long_no_title(interact, mock_context: MockContext):
    await mock_context.prepare_context('pt_BR')
    response: Response = await interact.add._callback(
            self=interact,
            ctx=mock_context,
            content="a" * 451
    )
    assert response.response_string == 'A mensagem deve ter no máximo 450 caracteres.'
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_annotations_add_content_title(interact, mock_context: MockContext):
    await mock_context.prepare_context('pt_BR')
    response: Response = await interact.add._callback(
            self=interact,
            ctx=mock_context,
            content='title:"title easier to remember" '
                    'A note about something I want to be able to check forever.'
    )
    assert response.response_string == 'Nota criada com sucesso. 📝 (ID: 1)'
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_annotations_add_content_title_too_long(interact, mock_context: MockContext):
    await mock_context.prepare_context('pt_BR')
    response: Response = await interact.add._callback(
            self=interact,
            ctx=mock_context,
            content='title:"title to make it easier to remember the content" '
                    'A note about something I want to be able to check forever.'
    )
    assert response.response_string == 'O título deve ter um máximo de 32 caracteres.'
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_annotations_check_wrong_id(interact, mock_context: MockContext):
    await mock_context.prepare_context('pt_BR')
    response: Response = await interact.check._callback(
            self=interact,
            ctx=mock_context,
            content='title'
    )
    assert response.response_string == 'title não é um ID valido.'
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_annotations_check_no_content_no_annotations(interact, mock_context: MockContext):
    await mock_context.prepare_context('pt_BR')
    response: Response = await interact.check._callback(
            self=interact,
            ctx=mock_context,
            content=''
    )
    assert response.response_string == 'Você não tem nenhuma anotação salva.'
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_annotations_check_one_annotation(interact, mock_context: MockContext):
    await mock_context.prepare_context('pt_BR')
    content = "a note about something I want to be able to check forever."
    title = "a" * 32
    await Annotation.create(content=content, user=mock_context.user, title=title)
    response: Response = await interact.check._callback(
            self=interact,
            ctx=mock_context,
            content=''
    )
    assert response.response_string == 'Suas anotações são aquelas com ID: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa [1]'
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_annotations_check_two_annotation(interact, mock_context: MockContext):
    await mock_context.prepare_context('pt_BR')
    content = "a note about something I want to be able to check forever."
    title = "a" * 32
    await Annotation.create(content=content, user=mock_context.user, title=title)
    content = "a note able to check forever."
    title = "a" * 32
    await Annotation.create(content=content, user=mock_context.user, title=title)
    response: Response = await interact.check._callback(
            self=interact,
            ctx=mock_context,
            content=''
    )
    assert response.response_string == ('Suas anotações são aquelas com ID: '
                                        'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa [1], '
                                        'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa [2]')
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_annotations_check_annotation_id_one(interact, mock_context: MockContext):
    await mock_context.prepare_context('pt_BR')
    content = "a note about something I want to be able to check forever."
    title = "a" * 32
    await Annotation.create(content=content, user=mock_context.user, title=title)
    content = "a note able to check forever."
    title = "a" * 32
    await Annotation.create(content=content, user=mock_context.user, title=title)
    response: Response = await interact.check._callback(
            self=interact,
            ctx=mock_context,
            content='1'
    )
    assert response.response_string == 'a note about something I want to be able to check forever.'
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_annotations_check_annotation_id_two(interact, mock_context: MockContext):
    await mock_context.prepare_context('pt_BR')
    content = "a note about something I want to be able to check forever."
    title = "a" * 32
    await Annotation.create(content=content, user=mock_context.user, title=title)
    content = "a note able to check forever."
    title = "a" * 32
    await Annotation.create(content=content, user=mock_context.user, title=title)
    response: Response = await interact.check._callback(
            self=interact,
            ctx=mock_context,
            content='2'
    )
    assert response.response_string == 'a note able to check forever.'
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_annotations_check_annotation_wrong_id(interact, mock_context: MockContext):
    await mock_context.prepare_context('pt_BR')
    content = "a note about something I want to be able to check forever."
    title = "a" * 32
    await Annotation.create(content=content, user=mock_context.user, title=title)
    content = "a note able to check forever."
    title = "a" * 32
    await Annotation.create(content=content, user=mock_context.user, title=title)
    response: Response = await interact.check._callback(
            self=interact,
            ctx=mock_context,
            content='3'
    )
    assert response.response_string == 'Você não tem nenhuma anotação com ID 3.'
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_annotations_delete_no_id(interact, mock_context: MockContext):
    await mock_context.prepare_context('pt_BR')
    content = "a note about something I want to be able to check forever."
    title = "a" * 32
    await Annotation.create(content=content, user=mock_context.user, title=title)
    content = "a note able to check forever."
    title = "a" * 32
    await Annotation.create(content=content, user=mock_context.user, title=title)
    response: Response = await interact.delete._callback(
            self=interact,
            ctx=mock_context,
            content=''
    )
    assert response.response_string == 'Você precisa fornecer um ID numérico válido.'
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_annotations_delete_id(interact, mock_context: MockContext):
    await mock_context.prepare_context('pt_BR')
    content = "a note about something I want to be able to check forever."
    title = "a" * 32
    await Annotation.create(content=content, user=mock_context.user, title=title)
    content = "a note able to check forever."
    title = "a" * 32
    await Annotation.create(content=content, user=mock_context.user, title=title)
    response: Response = await interact.delete._callback(
            self=interact,
            ctx=mock_context,
            content='1'
    )
    assert response.response_string == 'Sua anotação com ID 1 foi excluída com sucesso. 🗑'
    mock_context.reset_mock()
    del response
