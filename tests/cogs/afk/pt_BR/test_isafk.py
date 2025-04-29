# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.afk.commands.isafk import IsAfkCmd
from bot.translations import Response
from tests.helpers.mock_classes import MockContext


@pytest_asyncio.fixture
async def interact(mock_bot):
    return IsAfkCmd(bot=mock_bot)


@pytest.fixture
def mock_context(mock_bot):
    return MockContext("username", 12345, "channelname", 123456, mock_bot)


@pytest.mark.asyncio
async def test_isafk_own_user(interact, mock_context: MockContext):
    await mock_context.prepare_context('pt_BR')
    response: Response = await interact.isafk._callback(self=interact, ctx=mock_context, content="username")
    assert response.response_string == 'você não está afk... obviamente.'
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_isafk_bot_nick(interact, mock_context: MockContext):
    await mock_context.prepare_context('pt_BR')
    response: Response = await interact.isafk._callback(self=interact, ctx=mock_context, content="bot_name")
    assert response.response_string == 'Estou sempre aqui... assistindo.'
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_isafk_no_content(interact, mock_context: MockContext):
    await mock_context.prepare_context('pt_BR')
    response: Response = await interact.isafk._callback(self=interact, ctx=mock_context, content="status_user_50")
    assert response.response_string == '@status_user_50 está ausente 🏃⌨'
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_isafk_content(interact, mock_context: MockContext):
    await mock_context.prepare_context('pt_BR')
    response: Response = await interact.isafk._callback(self=interact, ctx=mock_context, content="status_user_51")
    assert response.response_string == '@status_user_51 está ausente 🏃⌨ e deixou uma nota: content'
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_isafk_user_dont_exist(interact, mock_context: MockContext):
    await mock_context.prepare_context('pt_BR')
    response: Response = await interact.isafk._callback(self=interact, ctx=mock_context, content="not_user_1234")
    assert response.response_string == 'Não me lembro de ter visto nenhum @not_user_1234.'
    mock_context.reset_mock()
    del response


