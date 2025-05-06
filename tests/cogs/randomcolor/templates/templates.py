# -*- coding: utf-8 -*-

from unittest.mock import patch

import pytest
import pytest_asyncio

from bot.cogs.randomcolor.command.randomcolor import RandomColorCmd
from bot.translations import Response
from tests.helpers.mock_classes import MockContext


@pytest_asyncio.fixture
async def interact(mock_bot):
    return RandomColorCmd(bot=mock_bot)


@pytest.mark.template
@pytest.mark.asyncio
async def test_randomcolor(
    interact, mock_context: MockContext, lang: str, content: str, expected: str, return_value: str | None
):
    await mock_context.prepare_context(lang)
    with patch("bot.apis.color.Color.name", return_value=return_value):
        response: Response = await interact.randomcolor._callback(self=interact, ctx=mock_context, tipo=content)
    assert response.response_string == expected, f"Expected {expected!r}, got: {response.response_string!r}"
