import pytest

from bot.ext import Response
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.alias.remove.test_params import Params


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang, interact=interact)
    mock_context.Asserter.assert_string(interact.translations.Remove.deco_usage("+"), usage)
    mock_context.Asserter.assert_string(interact.translations.Remove.deco_helper("+"), helper)


async def alias_remove(
    interact,
    mock_context: MockContext,
    lang: str,
    content: list[str],
    expected: str,
    special_user: bool = False,
    success: bool = False,
):
    await mock_context.prepare_context(lang, interact=interact)
    await mock_context.prepare_alias(special_user)
    response: Response = await interact.remove_alias._callback(interact, mock_context, *content)  # NOQA
    mock_context.Asserter.assert_string(response.response_string, expected)
    mock_context.Asserter.assert_boolean(response.success, success)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.no_content)
async def test_no_content(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_remove(interact, mock_context, lang=lang, content=[], expected=expected, success=False)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.remove_no_alias)
async def test_remove_no_alias(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_remove(interact, mock_context, lang=lang, content=["Some_Alias"], expected=expected, success=False)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.remove_success)
async def test_remove_success(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_remove(interact, mock_context, lang=lang, content=["The_Tests_alias"], expected=expected, success=True)
