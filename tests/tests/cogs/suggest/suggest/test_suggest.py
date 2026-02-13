import pytest
import pytest_asyncio

from bot.cogs.suggest.command.suggest import SuggestCmd
from tests.helpers.mock_classes import MockContext

from .test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return SuggestCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang, interact=interact)
    mock_context.Asserter.assert_string(interact.translations.Suggest.deco_usage("+"), usage, strict=True)
    mock_context.Asserter.assert_string(
        interact.translations.Suggest.deco_helper("+"),
        helper,
        strict=True,
    )


# To lazy to make this tests too.

# async def base_bug(
#     interact, mock_context: MockContext, lang: str, content: str,
#     expected: str = None, re_expected: str = None, success: bool = False
# ):
#     await mock_context.prepare_context(lang)
#     response: Response = await interact.bug._callback(interact, mock_context, content=content)  # NOQA
#     mock_context.Asserter.assert_string(response.response_string, expected=expected, re_expected=re_expected)
#     mock_context.Asserter.assert_boolean(response.success, success)
#
#
# @pytest.mark.asyncio
# @pytest.mark.parametrize("lang, expected", Params.no_content)
# async def test_no_content(interact, mock_context: MockContext, lang: str, expected: str):
#     await base_bug(
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
#     await base_bug(
#         interact,
#         mock_context,
#         lang=lang,
#         content="",
#         expected=expected,
#         success=True
#     )
