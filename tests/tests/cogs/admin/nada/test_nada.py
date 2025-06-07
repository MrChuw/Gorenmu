# -*- coding: utf-8 -*-
import pytest

from bot.translations import Response
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.admin.nada.test_params import Params


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.nada)
async def test_nada(interact, mock_context: MockContext, lang: str, expected: str):
    await mock_context.prepare_context(lang)
    response: Response = await interact.nada._callback(self=interact, ctx=mock_context, args="")
    assert response.response_string == expected, f"Expected {expected!r}, got: {response.response_string!r}"
