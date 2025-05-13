# -*- coding: utf-8 -*-

from unittest.mock import patch

import pytest
import pytest_asyncio

from bot.cogs.alias.command.alias import AliasCmd
from bot.translations import Response
from tests.helpers.mock_classes import MockContext


@pytest_asyncio.fixture
async def interact(mock_bot):
    return AliasCmd(bot=mock_bot)


@pytest.mark.template
@pytest.mark.asyncio
async def test_alias(interact, mock_context: MockContext, lang: str, content: str, expected: list[str | int]):
    await mock_context.prepare_context(lang)
    response: Response = await interact.alias._callback(self=interact, ctx=mock_context, args=content)
    assert response.response_string == expected[0], f"Expected {expected[0]!r}, got: {response.response_string!r}"
    assert (
        mock_context.simple_response.call_count == expected[1]
    ), f"Expected {expected[1]!r} function call, got: {mock_context.simple_response.call_count!r}"
    simple_response = mock_context.simple_response.call_args_list[0][0][1]
    assert simple_response == expected[2], f"Expected {expected[2]!r}, got: {simple_response!r}"


























