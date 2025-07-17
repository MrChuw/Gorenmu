import pytest

from bot.translations import Response
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.alias.link.test_params import Params


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    decorator = mock_context.bot.TranslationManager.get_decorator(interact.link_alias, mock_context)
    mock_context.Asserter.assert_string(decorator.usage, usage)
    mock_context.Asserter.assert_string(decorator.helper, helper)


async def alias_link(
    interact, mock_context: MockContext, lang: str, content: list[str], expected: str, special_user: bool = False
):
    await mock_context.prepare_context(lang)
    await mock_context.prepare_alias(special_user)
    response: Response = await interact.link_alias._callback(interact, mock_context, *content)  # NOQA
    mock_context.Asserter.assert_string(response.response_string, expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.no_content)
async def test_no_content(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_link(interact, mock_context, lang=lang, content=[], expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.alias_conflict)
async def test_alias_conflict(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_link(
        interact, mock_context, lang=lang, content=["Wrong_username", "The_Tests_alias"], expected=expected
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.name_conflict)
async def test_name_conflict(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_link(
        interact,
        mock_context,
        lang=lang,
        content=["Wrong_username", "The_Tests_alias", "The_Tests_alias"],
        expected=expected,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.wrong_username)
async def test_wrong_username(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_link(interact, mock_context, lang=lang, content=["Wrong_username", "."], expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.user_no_alias)
async def test_user_no_alias(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_link(
        interact,
        mock_context,
        lang=lang,
        special_user=True,
        content=["The_Tests_user", "The_Alias_"],
        expected=expected,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.user_link_to_link)
async def test_user_link_to_link(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_link(
        interact,
        mock_context,
        lang=lang,
        special_user=True,
        content=["The_Tests_user", "The_Alias_link_link"],
        expected=expected,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.user_link_to_link_custom_name)
async def test_user_link_to_link_custom_name(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_link(
        interact,
        mock_context,
        lang=lang,
        special_user=True,
        content=["The_Tests_user", "The_Alias_link_link", "Custom_Name"],
        expected=expected,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.user_alias_success)
async def test_user_alias_success(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_link(
        interact, mock_context, lang=lang, content=["some_user_45", "The_Tests_alias45"], expected=expected
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.user_alias_custom_name_success)
async def test_user_alias_custom_name_success(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_link(
        interact,
        mock_context,
        lang=lang,
        content=["some_user_45", "The_Tests_alias45", "Custom_Name"],
        expected=expected,
    )
