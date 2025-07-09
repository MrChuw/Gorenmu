# -*- coding: utf-8 -*-


import pytest
import pytest_asyncio

from bot.cogs.annotations.command.annotations import AnnotationsCmd
from bot.models import Annotation
from bot.translations import Response
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.annotations.check.test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return AnnotationsCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    decorator = mock_context.bot.TranslationManager.get_decorator(interact.check, mock_context)
    mock_context.Asserter.assert_string(decorator.usage, usage)
    mock_context.Asserter.assert_string(decorator.helper, helper)


async def base_annotations_check(
    interact, mock_context: MockContext, lang: str, content: str, expected: str, amount: int = 0
):
    await mock_context.prepare_context(lang)
    for value in range(amount):
        content_note = f"a note about something I want to be able to check forever. {value}"
        title = "a" * 32
        await Annotation.create(content=content_note, user=mock_context.user, title=title)
    response: Response = await interact.check._callback(self=interact, ctx=mock_context, content=content)  # NOQA
    mock_context.Asserter.assert_string(response.response_string, expected)


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
