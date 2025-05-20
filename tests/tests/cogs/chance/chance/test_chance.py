# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.chance.command.chance import ChanceCmd
from bot.translations import Response
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.chance.chance.test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return ChanceCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.chance)
async def test_chance(interact, mock_context: MockContext, lang: str, expected: str):
    await mock_context.prepare_context(lang)
    response: Response = await interact.chance._callback(self=interact, ctx=mock_context)
    assert response.response_string == expected, f"Expected {expected!r}, got: {response.response_string!r}"
