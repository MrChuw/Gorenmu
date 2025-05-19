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
@pytest.mark.parametrize("lang, expected", Params.no_content)
async def test_no_content(interact, mock_context: MockContext, lang: str, expected: str):
    await mock_context.prepare_context(lang)
    mock_context.invoke_by = "afk"
    response: Response = await interact.afk._callback(self=interact, ctx=mock_context)
    assert response.response_string == expected, f"Expected {expected!r}, got: {response.response_string!r}"


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.content)
async def test_afk_content(interact, mock_context: MockContext, lang: str, expected: str):
    await mock_context.prepare_context(lang)
    mock_context.invoke_by = "afk"
    response: Response = await interact.afk._callback(self=interact, ctx=mock_context, content="Just a test")
    assert response.response_string == expected, f"Expected {expected!r}, got: {response.response_string!r}"


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.too_much_content)
async def test_afk_too_much_content(interact, mock_context: MockContext, lang: str, expected: str):
    await mock_context.prepare_context(lang)
    mock_context.invoke_by = "afk"
    response: Response = await interact.afk._callback(self=interact, ctx=mock_context, content="a" * 500)
    assert response.response_string == expected, f"Expected {expected!r}, got: {response.response_string!r}"
