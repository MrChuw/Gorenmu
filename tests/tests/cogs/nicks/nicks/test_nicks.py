import pytest
import pytest_asyncio

from bot.cogs.nicks.command.nicks import NicksCmd
from tests.helpers.mock_classes import MockContext

from .test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return NicksCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang, interact=interact)
    mock_context.Asserter.assert_string(interact.translations.Nicks.deco_usage("+"), usage, strict=True)
    mock_context.Asserter.assert_string(interact.translations.Nicks.deco_helper("+"), helper, strict=True)


async def base_nicks(
    interact,
    mock_context: MockContext,
    lang: str,
    content: str,
    expected: str | None = None,
    re_expected: str | None = None,
    success: bool = False,
):
    await mock_context.prepare_context(lang, interact=interact)
    response: Response = await interact.nicks._callback(interact, mock_context, content)  # NOQA
    mock_context.Asserter.assert_string(response.response_string, expected=expected, re_expected=re_expected)
    mock_context.Asserter.assert_boolean(response.success, success)


# @pytest.mark.asyncio
# @pytest.mark.parametrize("lang, expected", Params.no_content)
# async def test_no_content(interact, mock_context: MockContext, lang: str, expected: str):
#     await base_nicks(
#         interact,
#         mock_context,
#         lang=lang,
#         content="",
#         expected=expected,
#         success=True
#     )
#
#
# @pytest.mark.asyncio
# @pytest.mark.parametrize("lang, expected", Params.no_content)
# async def test_(interact, mock_context: MockContext, lang: str, expected: str):
#     await base_nicks(
#         interact,
#         mock_context,
#         lang=lang,
#         content="",
#         expected=expected,
#         success=True
#     )
