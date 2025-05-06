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


@pytest.mark.template
@pytest.mark.asyncio
async def test_annotations(interact, mock_context: MockContext, lang: str, content: str, expected: list[str | int]):
    await mock_context.prepare_context(lang)
    response: Response = await interact.annotations._callback(self=interact, ctx=mock_context)

    assert response.response_string == expected[0], f"Expected {expected[0]!r}, got: {response.response_string!r}"
    assert (
        mock_context.simple_response.call_count == expected[1]
    ), f"Expected {expected[1]!r} function call, got: {mock_context.simple_response.call_count!r}"
    simple_response = mock_context.simple_response.call_args_list[0][0][1]
    assert simple_response == expected[2], f"Expected {expected[2]!r}, got: {simple_response!r}"


@pytest.mark.template
@pytest.mark.asyncio
async def test_annotations_add(interact, mock_context: MockContext, lang: str, content: str, expected: str):
    await mock_context.prepare_context(lang)
    response: Response = await interact.add._callback(self=interact, ctx=mock_context, content=content)
    assert response.response_string == expected, f"Expected {expected!r}, got: {response.response_string!r}"


@pytest.mark.template
@pytest.mark.asyncio
async def test_annotations_check(
    interact, mock_context: MockContext, lang: str, content: str, expected: str, amount: int = 0
):
    await mock_context.prepare_context(lang)
    for value in range(amount):
        content_note = f"a note about something I want to be able to check forever. {value}"
        title = "a" * 32
        await Annotation.create(content=content_note, user=mock_context.user, title=title)
    response: Response = await interact.check._callback(self=interact, ctx=mock_context, content=content)
    assert response.response_string == expected, f"Expected {expected!r}, got: {response.response_string!r}"


@pytest.mark.template
@pytest.mark.asyncio
async def test_annotations_delete(
    interact, mock_context: MockContext, lang: str, content: str, expected: str, amount: int = 0
):
    await mock_context.prepare_context(lang)
    for value in range(amount):
        content_note = f"a note about something I want to be able to check forever. {value}"
        title = "a" * 32
        await Annotation.create(content=content_note, user=mock_context.user, title=title)
    response: Response = await interact.delete._callback(self=interact, ctx=mock_context, content=content)
    assert response.response_string == expected, f"Expected {expected!r}, got: {response.response_string!r}"
