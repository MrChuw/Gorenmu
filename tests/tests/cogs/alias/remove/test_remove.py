import pytest

from bot.translations import Response
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.alias.remove.test_params import Params


async def alias_remove(
    interact, mock_context: MockContext, lang: str, content: list[str], expected: str, special_user: bool = False
):
    await mock_context.prepare_context(lang)
    await mock_context.prepare_alias(special_user)
    response: Response = await interact.remove_alias._callback(interact, mock_context, *content)  # NOQA
    assert response.response_string == expected, f"Expected {expected!r}, got: {response.response_string!r}"


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.no_content)
async def test_no_content(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_remove(interact, mock_context, lang=lang, content=[], expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.remove_no_alias)
async def test_remove_no_alias(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_remove(interact, mock_context, lang=lang, content=["Some_Alias"], expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.remove_success)
async def test_remove_success(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_remove(interact, mock_context, lang=lang, content=["The_Tests_alias"], expected=expected)
