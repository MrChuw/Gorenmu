# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.choice.command.choice import ChoiceCmd
from bot.translations import Response
from tests.helpers.mock_classes import MockContext


@pytest_asyncio.fixture
async def interact(mock_bot):
    return ChoiceCmd(bot=mock_bot)


@pytest.fixture
def mock_context(mock_bot):
    return MockContext("username", 12345, "channelname", 123456, mock_bot)


@pytest.mark.asyncio
async def test_choice_or(interact, mock_context: MockContext):
    await mock_context.prepare_context('pt_BR')
    response: Response = await interact.choice._callback(self=interact, ctx=mock_context, content="1 ou 2 ou 3")
    assert response.response_string == "2"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_choice_space(interact, mock_context: MockContext):
    await mock_context.prepare_context('pt_BR')
    response: Response = await interact.choice._callback(self=interact, ctx=mock_context, content="1 2 3")
    assert response.response_string == "2"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_choice_comma(interact, mock_context: MockContext):
    await mock_context.prepare_context('pt_BR')
    response: Response = await interact.choice._callback(self=interact, ctx=mock_context, content="1, 2, 3")
    assert response.response_string == "2"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_choice_mixed(interact, mock_context: MockContext):
    await mock_context.prepare_context('pt_BR')
    response: Response = await interact.choice._callback(self=interact, ctx=mock_context, content="1 ou 2, 3 4")
    assert response.response_string == "4"
    mock_context.reset_mock()
    del response
