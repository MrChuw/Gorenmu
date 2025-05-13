# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.chance.command.chance import ChanceCmd
from bot.translations import Response
from tests.helpers.mock_classes import MockContext


@pytest_asyncio.fixture
async def interact(mock_bot):
    return ChanceCmd(bot=mock_bot)


@pytest.mark.template
@pytest.mark.asyncio
async def test_choice(interact, mock_context: MockContext, lang: str, content: str, expected: str):
    await mock_context.prepare_context(lang)
    response: Response = await interact.chance._callback(self=interact, ctx=mock_context)
    assert response.response_string == expected, f"Expected {expected!r}, got: {response.response_string!r}"
