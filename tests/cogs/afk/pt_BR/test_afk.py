# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.afk.commands.afk import AFKCmd
from bot.translations import Response
from tests.helpers.mock_classes import MockContext


@pytest_asyncio.fixture
async def interact(mock_bot):
    return AFKCmd(bot=mock_bot)


@pytest.fixture
def mock_context(mock_bot):
    return MockContext("username", 12345, "channelname", 123456, mock_bot)


@pytest.mark.asyncio
async def test_afk_no_content(interact, mock_context: MockContext):
    await mock_context.prepare_context('pt_BR')
    mock_context.invoke_by = "afk"
    response: Response = await interact.afk._callback(self=interact, ctx=mock_context)
    assert response.response_string == 'você ficou ausente 🏃⌨'
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_afk_content(interact, mock_context: MockContext):
    await mock_context.prepare_context('pt_BR')
    mock_context.invoke_by = "afk"
    response: Response = await interact.afk._callback(self=interact, ctx=mock_context, content="Just a test")
    assert response.response_string == 'você ficou ausente 🏃⌨ e deixou uma nota com: Just a test'
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_afk_too_much_content(interact, mock_context: MockContext):
    await mock_context.prepare_context('pt_BR')
    mock_context.invoke_by = "afk"
    response: Response = await interact.afk._callback(self=interact, ctx=mock_context, content="a" * 500)
    assert response.response_string == 'A mensagem deve ter no máximo 450 caracteres.'
    mock_context.reset_mock()
    del response
