# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.afk.commands.afk import AFKCmd
from bot.translations import Response
from tests.helpers.mock_classes import MockContext


@pytest_asyncio.fixture
async def interact(mock_bot):
    return AFKCmd(bot=mock_bot)


@pytest.mark.template
@pytest.mark.asyncio
async def test_afk_no_content(interact, mock_context: MockContext, lang: str, expected: str):
    await mock_context.prepare_context(lang)
    mock_context.invoke_by = "afk"
    response: Response = await interact.afk._callback(self=interact, ctx=mock_context)
    assert response.response_string == expected, f"Expected {expected!r}, got: {response.response_string!r}"


@pytest.mark.template
@pytest.mark.asyncio
async def test_afk_content(interact, mock_context: MockContext, lang: str, content: str, expected: str):
    await mock_context.prepare_context(lang)
    mock_context.invoke_by = "afk"
    response: Response = await interact.afk._callback(self=interact, ctx=mock_context, content=content)
    assert response.response_string == expected, f"Expected {expected!r}, got: {response.response_string!r}"


@pytest.mark.template
@pytest.mark.asyncio
async def test_afk_too_much_content(interact, mock_context: MockContext, lang: str, content: str, expected: str):
    await mock_context.prepare_context(lang)
    mock_context.invoke_by = "afk"
    response: Response = await interact.afk._callback(self=interact, ctx=mock_context, content=content)
    assert response.response_string == expected, f"Expected {expected!r}, got: {response.response_string!r}"
