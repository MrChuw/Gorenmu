from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio

from bot.cogs.safebooru.command import safebooru
from tests.helpers.mock_classes import MockContext

from .test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return safebooru.SafeBooruCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang, interact=interact)
    mock_context.Asserter.assert_string(interact.translations.Safebooru.deco_usage("+"), usage)
    mock_context.Asserter.assert_string(interact.translations.Safebooru.deco_helper("+"), helper)


async def base_safebooru(
    interact,
    mock_context: MockContext,
    lang: str,
    content: str,
    expected: str | None = None,
    re_expected: str | None = None,
    success: bool = False,
):
    await mock_context.prepare_context(lang, interact=interact)
    response: Response = await interact.safebooru._callback(interact, mock_context, args=content)  # NOQA
    mock_context.Asserter.assert_string(response.response_string, expected=expected, re_expected=re_expected)
    mock_context.Asserter.assert_boolean(response.success, success)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.no_content)
async def test_no_content(interact, mock_context: MockContext, lang: str, expected: str):
    response = ["www.some_url.com"], ["www.some_url.com"]
    shortener_response = AsyncMock(return_value=response)
    with (
        patch("bot.apis.booru.Booru.Safebooru.random", new_callable=AsyncMock) as mock_booru,
        patch.object(
            safebooru,
            "shortener",
            new_callable=AsyncMock,
            side_effect=shortener_response,
        ),
    ):
        async with mock_context.MockBuilder.Asyncio.sleep_skip():
            mock_booru.return_value = response
            await base_safebooru(
                interact,
                mock_context,
                lang=lang,
                content="",
                expected=expected,
                success=True,
            )
