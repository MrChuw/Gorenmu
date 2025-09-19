import pytest

from bot.ext import Response
from tests.helpers.mock_classes import MockContext

from .test_params import Params


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    mock_context.Asserter.assert_string(interact.translations.Edit.deco_usage(mock_context, "+"), usage)
    mock_context.Asserter.assert_string(interact.translations.Edit.deco_helper(mock_context, "+"), helper)


async def alias_edit(
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
    response: Response = await interact.edit_alias._callback(interact, mock_context, *content)  # NOQA
    mock_context.Asserter.assert_string(response.response_string, expected)
    mock_context.Asserter.assert_boolean(response.success, success)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.no_content)
async def test_no_content(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_edit(interact, mock_context, lang=lang, content=[], expected=expected, success=False)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.wrong_name_no_command)
async def test_wrong_name_no_command(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_edit(interact, mock_context, lang=lang, content=["Wrong_alias"], expected=expected, success=False)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.wrong_name_wrong_command)
async def test_wrong_name_wrong_command(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_edit(
        interact, mock_context, lang=lang, content=["Wrong_alias", "chance"], expected=expected, success=False
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.name_wrong_command)
async def test_name_wrong_command(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_edit(
        interact,
        mock_context,
        lang=lang,
        content=["The_Tests_alias", "blablablablablablablablablablablabla"],
        expected=expected,
        success=False,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.alias_link_wrong_command)
async def test_alias_link_wrong_command(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_edit(
        interact,
        mock_context,
        lang=lang,
        special_user=True,
        content=["The_Link_alias", "chance"],
        expected=expected,
        success=False,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.guard_caught)
async def test_guard_caught(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_edit(
        interact, mock_context, lang=lang, content=["The_Tests_alias", "restart"], expected=expected, success=False
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.describe_success)
async def test_describe_success(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_edit(
        interact, mock_context, lang=lang, content=["The_Tests_alias", "chance"], expected=expected, success=False
    )
