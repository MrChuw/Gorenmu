# -*- coding: utf-8 -*-
import pytest

from bot.translations import Response
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.admin.nada.test_params import Params


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    decorator = mock_context.bot.TranslationManager.get_decorator(interact.nada, mock_context)
    mock_context.Asserter.assert_string(decorator.usage, usage)
    mock_context.Asserter.assert_string(decorator.helper, helper)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.nada)
async def test_nada(interact, mock_context: MockContext, lang: str, expected: str):
    await mock_context.prepare_context(lang)
    response: Response = await interact.nada._callback(self=interact, ctx=mock_context, args="")
    mock_context.Asserter.assert_string(response.response_string, expected)
