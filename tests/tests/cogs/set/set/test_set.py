# -*- coding: utf-8 -*-

import pytest

from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.set.set.test_params import Params


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    decorator = mock_context.bot.TranslationManager.get_decorator(interact.set, mock_context)
    mock_context.Asserter.assert_string(decorator.usage, usage)
    mock_context.Asserter.assert_string(decorator.helper, helper)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, args, expected", Params.set_base)
async def test_set(interact, mock_context: MockContext, lang: str, args: str, expected: str):
    await mock_context.prepare_context(lang)
    response = await interact.set._callback(self=interact, ctx=mock_context, args=args)
    mock_context.Asserter.assert_string(response.response_string, expected)
