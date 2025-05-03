# -*- coding: utf-8 -*-
import random

import pytest
import pytest_asyncio

from bot.cogs.chance.command.chance import ChanceCmd
from bot.translations import Response
from tests.helpers.mock_classes import MockContext


@pytest_asyncio.fixture
async def interact(mock_bot):
    return ChanceCmd(bot=mock_bot)


@pytest.fixture
def mock_context(mock_bot):
    return MockContext("username", 12345, "channelname", 123456, mock_bot)  # NOQA


@pytest.mark.asyncio
async def test_choice(interact, mock_context: MockContext):
    random.seed(0)
    await mock_context.prepare_context('en')
    response: Response = await interact.chance._callback(self=interact, ctx=mock_context)
    assert response.response_string == "84.44%", \
        f"Expected 84.44%, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response
