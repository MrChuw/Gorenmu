# -*- coding: utf-8 -*-
import pytest
import pytest_asyncio

from bot.cogs.afk.commands.afk import AFKCmd
from bot.translations import Response
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.afk.afk.test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return AFKCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    decorator = mock_context.bot.TranslationManager.get_decorator(interact.afk, mock_context)
    mock_context.Asserter.assert_string(decorator.usage, usage)
    mock_context.Asserter.assert_string(decorator.helper, helper)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.no_content)
async def test_no_content(interact, mock_context: MockContext, lang: str, expected: str):
    await mock_context.prepare_context(lang)
    mock_context.invoke_by = "afk"
    response: Response = await interact.afk._callback(self=interact, ctx=mock_context)
    mock_context.Asserter.assert_string(response.response_string, expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.content)
async def test_afk_content(interact, mock_context: MockContext, lang: str, expected: str):
    await mock_context.prepare_context(lang)
    mock_context.invoke_by = "afk"
    response: Response = await interact.afk._callback(self=interact, ctx=mock_context, content="Just a test")
    mock_context.Asserter.assert_string(response.response_string, expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.too_much_content)
async def test_afk_too_much_content(interact, mock_context: MockContext, lang: str, expected: str):
    await mock_context.prepare_context(lang)
    mock_context.invoke_by = "afk"
    response: Response = await interact.afk._callback(self=interact, ctx=mock_context, content="a" * 500)
    mock_context.Asserter.assert_string(response.response_string, expected)
