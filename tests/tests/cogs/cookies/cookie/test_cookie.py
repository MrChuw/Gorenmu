import pytest

from bot.cogs.cookies.command.cookies import CookieCmd
from bot.ext import Response
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.cookies.cookie.test_params import Params


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    mock_context.Asserter.assert_string(interact.translations.Cookies.deco_usage(mock_context, "+"), usage)
    mock_context.Asserter.assert_string(interact.translations.Cookies.deco_helper(mock_context, "+"), helper)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.cookie)
async def test_cookie(interact: CookieCmd, mock_context: MockContext, lang: str, expected: str):
    await mock_context.prepare_context(lang)
    response: Response = await interact.cookies._callback(self=interact, ctx=mock_context)
    assert response.response_string == expected, f"Expected {expected!r}, got: {response.response_string!r}"
    mock_context.Asserter.assert_boolean(response.success, False)
