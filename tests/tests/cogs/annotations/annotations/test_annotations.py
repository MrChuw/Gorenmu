# -*- coding: utf-8 -*-


import pytest
import pytest_asyncio

from bot.cogs.annotations.command.annotations import AnnotationsCmd
from bot.ext import Response
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.annotations.annotations.test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return AnnotationsCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    mock_context.Asserter.assert_string(interact.translations.Annotations.deco_usage(mock_context, "+"), usage)
    mock_context.Asserter.assert_string(interact.translations.Annotations.deco_helper(mock_context, "+"), helper)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.annotations)
async def test_annotations(interact, mock_context: MockContext, lang: str, expected: list[str | int]):
    await mock_context.prepare_context(lang)
    response: Response = await interact.annotations._callback(self=interact, ctx=mock_context)

    mock_context.Asserter.assert_string(response.response_string, expected[0])
    mock_context.Asserter.assert_number(mock_context.simple_response.call_count, expected[1])
    simple_response = mock_context.simple_response.call_args_list[0][0][1]
    mock_context.Asserter.assert_string(simple_response, expected[2])
    mock_context.Asserter.assert_boolean(response.success, True)
