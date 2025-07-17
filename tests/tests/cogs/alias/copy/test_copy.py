# -*- coding: utf-8 -*-

import pytest

from bot.translations import Response
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.alias.copy.test_params import Params


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    decorator = mock_context.bot.TranslationManager.get_decorator(interact.copy_alias, mock_context)
    mock_context.Asserter.assert_string(decorator.usage, usage)
    mock_context.Asserter.assert_string(decorator.helper, helper)


async def alias_copy(
    interact, mock_context: MockContext, lang: str, content: list[str], expected: str, special_user: bool = False
):
    await mock_context.prepare_context(lang)
    await mock_context.prepare_alias(special_user)
    response: Response = await interact.copy_alias._callback(interact, mock_context, *content)  # NOQA
    mock_context.Asserter.assert_string(response.response_string, expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.no_content)
async def test_no_content(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_copy(interact, mock_context, lang=lang, content=[""], expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.user_no_alias)
async def test_user_no_alias(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_copy(interact, mock_context, lang=lang, content=["The_Tests_user"], expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.user_invalid_alias)
async def test_user_invalid_alias(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_copy(interact, mock_context, lang=lang, content=["The_Tests_user", "Invalid_alias#"], expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.user_alias_conflict)
async def test_user_alias_conflict(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_copy(
        interact, mock_context, lang=lang, content=["The_Tests_user", "The_Tests_alias"], expected=expected
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.user_not_found)
async def test_user_not_found(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_copy(interact, mock_context, lang=lang, content=["The_Tests_ser", "Invalid_alias"], expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.user_alias_not_found)
async def test_user_alias_not_found(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_copy(
        interact,
        mock_context,
        lang=lang,
        special_user=True,
        content=["The_Tests_user", "Invalid_alias"],
        expected=expected,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.user_alias_link)
async def test_user_alias_link(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_copy(
        interact,
        mock_context,
        lang=lang,
        special_user=True,
        content=["The_Tests_user", "The_Alias_link"],
        expected=expected,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.user_alias_success)
async def test_user_alias_success(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_copy(
        interact,
        mock_context,
        lang=lang,
        special_user=True,
        content=["The_Tests_user", "The_Alias_test"],
        expected=expected,
    )
