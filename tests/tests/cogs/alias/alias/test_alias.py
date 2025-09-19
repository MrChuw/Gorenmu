# -*- coding: utf-8 -*-

import pytest

from bot.translations import Response
from tests.helpers.mock_classes import MockContext

from .test_alias_params import Params


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    mock_context.Asserter.assert_string(interact.translations.Alias.deco_usage(mock_context, "+"), usage)
    mock_context.Asserter.assert_string(interact.translations.Alias.deco_helper(mock_context, "+"), helper)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.params_alias)
async def test_alias(interact, mock_context: MockContext, lang: str, expected: list[str | int]):
    await mock_context.prepare_context(lang)
    response: Response = await interact.alias._callback(self=interact, ctx=mock_context, args="")
    mock_context.Asserter.assert_string(response.response_string, expected[0])
    mock_context.Asserter.assert_number(mock_context.simple_response.call_count, expected[1])
    simple_response = mock_context.simple_response.call_args_list[0][0][1]
    mock_context.Asserter.assert_string(simple_response, expected[2])
    mock_context.Asserter.assert_boolean(response.success, False)
