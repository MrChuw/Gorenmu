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
    return MockContext("username", 12345, "channelname", 123456, mock_bot)  # NOQA


@pytest.mark.asyncio
async def test_annotations(interact, mock_context: MockContext):
    await mock_context.prepare_context('en')
    response: Response = await interact.annotations._callback(self=interact, ctx=mock_context)
    assert response.response_string == "", \
        f"Expected a empty string, got: {response.response_string!r}"
    assert mock_context.simple_response.call_count == 1, \
        f"Expected one call for function simple response, got: {mock_context.simple_response.call_count!r}"
    assert mock_context.simple_response.call_args_list[0][0][1] == "Shush", \
        f"Expected a Shush, got: {mock_context.simple_response.call_args_list[0][0][1]!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_annotations_add_no_content(interact, mock_context: MockContext):
    await mock_context.prepare_context('en')
    response: Response = await interact.add._callback(self=interact, ctx=mock_context, content="")
    assert response.response_string == 'You need to provide content for this command.', \
        f"Expected a error message, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_annotations_add_content_no_title(interact, mock_context: MockContext):
    await mock_context.prepare_context('en')
    response: Response = await interact.add._callback(
            self=interact,
            ctx=mock_context,
            content="A note about something I want to be able to check forever."
    )
    assert response.response_string == 'Note successfully created. 📝 (ID: 1)', \
        f"Expected a successful message with a ID, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_annotations_add_content_too_long_no_title(interact, mock_context: MockContext):
    await mock_context.prepare_context('en')
    response: Response = await interact.add._callback(
            self=interact,
            ctx=mock_context,
            content="a" * 451
    )
    assert response.response_string == 'The message must have a maximum of 450 characters.', \
        f"Expected a error message, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_annotations_add_content_title(interact, mock_context: MockContext):
    await mock_context.prepare_context('en')
    response: Response = await interact.add._callback(
            self=interact,
            ctx=mock_context,
            content='title:"title easier to remember" '
                    'A note about something I want to be able to check forever.'
    )
    assert response.response_string == 'Note successfully created. 📝 (ID: 1)', \
        f"Expected a successful message with a ID, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_annotations_add_content_title_too_long(interact, mock_context: MockContext):
    await mock_context.prepare_context('en')
    response: Response = await interact.add._callback(
            self=interact,
            ctx=mock_context,
            content='title:"title to make it easier to remember the content" '
                    'A note about something I want to be able to check forever.'
    )
    assert response.response_string == 'The title must have a maximum of 32 characters.', \
        f"Expected a error message, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_annotations_check_wrong_id(interact, mock_context: MockContext):
    await mock_context.prepare_context('en')
    response: Response = await interact.check._callback(
            self=interact,
            ctx=mock_context,
            content='title'
    )
    assert response.response_string == 'title is not a valid ID.', \
        f"Expected a error message, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_annotations_check_no_content_no_annotations(interact, mock_context: MockContext):
    await mock_context.prepare_context('en')
    response: Response = await interact.check._callback(
            self=interact,
            ctx=mock_context,
            content=''
    )
    assert response.response_string == 'You don\'t have any annotations saved.', \
        f"Expected a message saying that user has no annotations, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_annotations_check_one_annotation(interact, mock_context: MockContext):
    await mock_context.prepare_context('en')
    content = "a note about something I want to be able to check forever."
    title = "a" * 32
    await Annotation.create(content=content, user=mock_context.user, title=title)
    response: Response = await interact.check._callback(
            self=interact,
            ctx=mock_context,
            content=''
    )
    assert response.response_string == 'Your annotations are the ones with ID: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa [1]', \
        f"Expected a message with \"a\"'s and ID 1, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_annotations_check_two_annotation(interact, mock_context: MockContext):
    await mock_context.prepare_context('en')
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
    assert response.response_string == ('Your annotations are the ones with ID: '
                                        'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa [1], '
                                        'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa [2]'), \
        f"Expected two messages with \"a\"'s and ID 1 and 2, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_annotations_check_annotation_id_one(interact, mock_context: MockContext):
    await mock_context.prepare_context('en')
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
    assert response.response_string == 'a note about something I want to be able to check forever.', \
        f"Expected a message with the content of annotation, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_annotations_check_annotation_id_two(interact, mock_context: MockContext):
    await mock_context.prepare_context('en')
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
    assert response.response_string == 'a note able to check forever.', \
        f"Expected a message with the content of annotation, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_annotations_check_annotation_wrong_id(interact, mock_context: MockContext):
    await mock_context.prepare_context('en')
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
    assert response.response_string == 'You don\'t have any annotation with ID 3.', \
        f"Expected a error message of not having ID 3 annotation, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_annotations_delete_no_id(interact, mock_context: MockContext):
    await mock_context.prepare_context('en')
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
    assert response.response_string == 'You need to provide a valid numeric ID.', \
        f"Expected a error message of not having provided a ID, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_annotations_delete_id(interact, mock_context: MockContext):
    await mock_context.prepare_context('en')
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
    assert response.response_string == 'Your annotation with ID 1 was successfully deleted. 🗑', \
        f"Expected a message about the annotation deletion, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response
