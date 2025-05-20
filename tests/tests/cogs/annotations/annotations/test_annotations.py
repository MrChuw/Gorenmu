# -*- coding: utf-8 -*-


import pytest
import pytest_asyncio

from bot.cogs.annotations.command.annotations import AnnotationsCmd
from bot.models import Annotation
from bot.translations import Response
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.annotations.annotations.test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return AnnotationsCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.annotations)
async def test_annotations(interact, mock_context: MockContext, lang: str, expected: list[str | int]):
    await mock_context.prepare_context(lang)
    response: Response = await interact.annotations._callback(self=interact, ctx=mock_context)

    assert response.response_string == expected[0], f"Expected {expected[0]!r}, got: {response.response_string!r}"
    assert (
        mock_context.simple_response.call_count == expected[1]
    ), f"Expected {expected[1]!r} function call, got: {mock_context.simple_response.call_count!r}"
    simple_response = mock_context.simple_response.call_args_list[0][0][1]
    assert simple_response == expected[2], f"Expected {expected[2]!r}, got: {simple_response!r}"


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.annotations)
async def base_annotations_add(interact, mock_context: MockContext, lang: str, content: str, expected: str):
    await mock_context.prepare_context(lang)
    response: Response = await interact.add._callback(self=interact, ctx=mock_context, content=content)  # NOQA
    assert response.response_string == expected, f"Expected {expected!r}, got: {response.response_string!r}"


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.add_no_content)
async def add_no_content(interact, mock_context: MockContext, lang: str, expected: str):
    await base_annotations_add(interact, mock_context, lang=lang, content="", expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.add_content_no_title)
async def add_content_no_title(interact, mock_context: MockContext, lang: str, expected: str):
    await base_annotations_add(
        interact,
        mock_context,
        lang=lang,
        content="A note about something I want to be able to check forever.",
        expected=expected,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.add_content_too_long_no_title)
async def add_content_too_long_no_title(interact, mock_context: MockContext, lang: str, expected: str):
    await base_annotations_add(interact, mock_context, lang=lang, content="a" * 451, expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.add_content_title)
async def add_content_title(interact, mock_context: MockContext, lang: str, expected: str):
    await base_annotations_add(
        interact,
        mock_context,
        lang=lang,
        content='title:"title easier to remember" A note about something I want to be able to check forever.',
        expected=expected,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.add_content_title_too_long)
async def add_content_title_too_long(interact, mock_context: MockContext, lang: str, expected: str):
    await base_annotations_add(
        interact,
        mock_context,
        lang=lang,
        content='title:"title to make it easier to remember the content" '
        "A note about something I want to be able to check forever.",
        expected=expected,
    )


async def base_annotations_check(
    interact, mock_context: MockContext, lang: str, content: str, expected: str, amount: int = 0
):
    await mock_context.prepare_context(lang)
    for value in range(amount):
        content_note = f"a note about something I want to be able to check forever. {value}"
        title = "a" * 32
        await Annotation.create(content=content_note, user=mock_context.user, title=title)
    response: Response = await interact.check._callback(self=interact, ctx=mock_context, content=content)  # NOQA
    assert response.response_string == expected, f"Expected {expected!r}, got: {response.response_string!r}"


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.check_wrong_id)
async def check_wrong_id(interact, mock_context: MockContext, lang: str, expected: str):
    await base_annotations_check(interact, mock_context, lang=lang, content="", expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.check_no_content_no_annotations)
async def check_no_content_no_annotations(interact, mock_context: MockContext, lang: str, expected: str):
    await base_annotations_check(interact, mock_context, lang=lang, content="", expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.check_one_annotation)
async def check_one_annotation(interact, mock_context: MockContext, lang: str, expected: str):
    await base_annotations_check(interact, mock_context, lang=lang, content="", expected=expected, amount=1)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.check_two_annotation)
async def check_two_annotation(interact, mock_context: MockContext, lang: str, expected: str):
    await base_annotations_check(interact, mock_context, lang=lang, content="", expected=expected, amount=2)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.check_annotation_id_one)
async def check_annotation_id_one(interact, mock_context: MockContext, lang: str, expected: str):
    await base_annotations_check(interact, mock_context, lang=lang, content="1", expected=expected, amount=2)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.check_annotation_id_two)
async def check_annotation_id_two(interact, mock_context: MockContext, lang: str, expected: str):
    await base_annotations_check(interact, mock_context, lang=lang, content="2", expected=expected, amount=2)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.check_annotation_wrong_id)
async def check_annotation_wrong_id(interact, mock_context: MockContext, lang: str, expected: str):
    await base_annotations_check(interact, mock_context, lang=lang, content="3", expected=expected, amount=2)


async def base_annotations_delete(interact, mock_context: MockContext, lang: str, content: str, expected, amount=0):
    await mock_context.prepare_context(lang)
    for value in range(amount):
        content_note = f"a note about something I want to be able to check forever. {value}"
        title = "a" * 32
        await Annotation.create(content=content_note, user=mock_context.user, title=title)
    response: Response = await interact.delete._callback(self=interact, ctx=mock_context, content=content)  # NOQA
    assert response.response_string == expected, f"Expected {expected!r}, got: {response.response_string!r}"


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.delete_no_id)
async def test_delete_no_id(interact, mock_context: MockContext, lang: str, expected: str):
    await base_annotations_delete(interact, mock_context, lang=lang, content="", expected=expected, amount=2)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.delete_id)
async def test_delete_id(interact, mock_context: MockContext, lang: str, expected: str):
    await base_annotations_delete(interact, mock_context, lang=lang, content="1", expected=expected, amount=2)
