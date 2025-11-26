import pytest

from bot.ext import Response
from tests.helpers.mock_classes import MockContext

from .test_params import Params


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    mock_context.Asserter.assert_string(interact.translations.Describe.deco_usage(mock_context, "+"), usage)
    mock_context.Asserter.assert_string(interact.translations.Describe.deco_helper(mock_context, "+"), helper)


async def alias_describe(
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
    response: Response = await interact.describe_alias._callback(interact, mock_context, *content)  # NOQA
    mock_context.Asserter.assert_string(response.response_string, expected)
    mock_context.Asserter.assert_boolean(response.success, success)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.no_content)
async def test_no_content(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_describe(interact, mock_context, lang=lang, content=[], expected=expected, success=False)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.wrong_alias_no_description)
async def test_wrong_alias_no_description(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_describe(
        interact,
        mock_context,
        lang=lang,
        content=["Some_alias"],
        expected=expected,
        success=False,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.alias_no_description)
async def test_alias_no_description(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_describe(
        interact,
        mock_context,
        lang=lang,
        content=["The_Tests_alias"],
        expected=expected,
        success=True,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.alias_description)
async def test_alias_description(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_describe(
        interact,
        mock_context,
        lang=lang,
        content=["The_Tests_alias", "Some_description"],
        expected=expected,
        success=True,
    )
