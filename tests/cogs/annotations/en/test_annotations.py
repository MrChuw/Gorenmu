# -*- coding: utf-8 -*-
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio

from bot.cogs.annotations.command.annotations import AnnotationsCmd
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
    await mock_context.prepare_context('en')
    response: Response = await interact.annotations._callback(self=interact, ctx=mock_context)
    assert response.response_string == ""
    assert mock_context.simple_response.call_count == 1
    assert mock_context.simple_response.call_args_list[0][0][1] == "Shush"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_annotations_no_content(interact, mock_context: MockContext):
    await mock_context.prepare_context('en')
    response: Response = await interact.add._callback(self=interact, ctx=mock_context, content="")
    assert response.response_string == 'You need to provide content for this command.'
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_annotations_content_no_title(interact, mock_context: MockContext):
    await mock_context.prepare_context('en')
    response: Response = await interact.add._callback(
            self=interact,
            ctx=mock_context,
            content="A note about something I want to be able to check forever."
    )
    assert response.response_string == 'Note successfully created. 📝 (ID: 1)'
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_annotations_content_too_long_no_title(interact, mock_context: MockContext):
    await mock_context.prepare_context('en')
    response: Response = await interact.add._callback(
            self=interact,
            ctx=mock_context,
            content="a" * 451
    )
    assert response.response_string == 'The message must have a maximum of 450 characters.'
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_annotations_content_title(interact, mock_context: MockContext):
    await mock_context.prepare_context('en')
    response: Response = await interact.add._callback(
            self=interact,
            ctx=mock_context,
            content='title:"title easier to remember" '
                    'A note about something I want to be able to check forever.'
    )
    assert response.response_string == 'Note successfully created. 📝 (ID: 1)'
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_annotations_content_title_too_long(interact, mock_context: MockContext):
    await mock_context.prepare_context('en')
    response: Response = await interact.add._callback(
            self=interact,
            ctx=mock_context,
            content='title:"title to make it easier to remember the content" '
                    'A note about something I want to be able to check forever.'
    )
    assert response.response_string == 'The title must have a maximum of 32 characters.'
    mock_context.reset_mock()
    del response





















