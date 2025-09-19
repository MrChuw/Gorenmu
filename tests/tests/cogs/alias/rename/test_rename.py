import pytest

from bot.translations import Response
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.alias.rename.test_params import Params


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    mock_context.Asserter.assert_string(interact.translations.Rename.deco_usage(mock_context, "+"), usage)
    mock_context.Asserter.assert_string(interact.translations.Rename.deco_helper(mock_context, "+"), helper)


async def alias_rename(
    interact,
    mock_context: MockContext,
    lang: str,
    content: list[str],
    expected: str,
    special_user: bool = False,
    success: bool = False,
):
    await mock_context.prepare_context(lang)
    await mock_context.prepare_alias(special_user)
    response: Response = await interact.rename_alias._callback(interact, mock_context, *content)  # NOQA
    mock_context.Asserter.assert_string(response.response_string, expected)
    mock_context.Asserter.assert_boolean(response.success, success)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.no_content)
async def test_no_content(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_rename(interact, mock_context, lang=lang, content=[], expected=expected, success=False)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.no_alias)
async def test_no_alias(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_rename(
        interact,
        mock_context,
        lang=lang,
        content=["Wrong_alias_name", "New_alias_name"],
        expected=expected,
        success=False,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.alias_conflict)
async def test_alias_conflict(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_rename(
        interact,
        mock_context,
        lang=lang,
        special_user=True,
        content=["The_Tests_alias", "The_Tests_user"],
        expected=expected,
        success=False,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.rename_success)
async def test_rename_success(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_rename(
        interact,
        mock_context,
        lang=lang,
        special_user=True,
        content=["The_Tests_alias", "The_new_name"],
        expected=expected,
        success=True,
    )
