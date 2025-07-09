# -*- coding: utf-8 -*-


import pytest
import pytest_asyncio

from bot.cogs.annotations.command.annotations import AnnotationsCmd
from bot.translations import Response
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.annotations.add.test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return AnnotationsCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    decorator = mock_context.bot.TranslationManager.get_decorator(interact.add, mock_context)
    mock_context.Asserter.assert_string(decorator.usage, usage)
    mock_context.Asserter.assert_string(decorator.helper, helper)


async def base_annotations_add(interact, mock_context: MockContext, lang: str, content: str, expected: str):
    await mock_context.prepare_context(lang)
    response: Response = await interact.add._callback(self=interact, ctx=mock_context, content=content)  # NOQA
    mock_context.Asserter.assert_string(response.response_string, expected)


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
