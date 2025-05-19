# -*- coding: utf-8 -*-

import pytest

from bot.translations import Response
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.alias.alias.test_alias_params import params_alias


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", params_alias)
async def test_alias(interact, mock_context: MockContext, lang: str, expected: list[str | int]):
    await mock_context.prepare_context(lang)
    response: Response = await interact.alias._callback(self=interact, ctx=mock_context, args="")
    assert response.response_string == expected[0], f"Expected {expected[0]!r}, got: {response.response_string!r}"
    assert (
        mock_context.simple_response.call_count == expected[1]
    ), f"Expected {expected[1]!r} function call, got: {mock_context.simple_response.call_count!r}"
    simple_response = mock_context.simple_response.call_args_list[0][0][1]
    assert simple_response == expected[2], f"Expected {expected[2]!r}, got: {simple_response!r}"
