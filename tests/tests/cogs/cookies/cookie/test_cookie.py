# -*- coding: utf-8 -*-

import pytest

from bot.cogs.cookies.command.cookies import CookieCmd
from bot.translations import Response
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.cookies.cookie.test_params import Params


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.cookie)
async def test_cookie(interact: CookieCmd, mock_context: MockContext, lang: str, expected: str):
    await mock_context.prepare_context(lang)
    response: Response = await interact.cookies._callback(self=interact, ctx=mock_context)
    assert response.response_string == expected, f"Expected {expected!r}, got: {response.response_string!r}"
