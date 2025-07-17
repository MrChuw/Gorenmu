# -*- coding: utf-8 -*-


import pytest

from bot.translations import Response
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.alias.describe.test_params import Params


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    decorator = mock_context.bot.TranslationManager.get_decorator(interact.describe_alias, mock_context)
    mock_context.Asserter.assert_string(decorator.usage, usage)
    mock_context.Asserter.assert_string(decorator.helper, helper)


async def alias_describe(
    interact, mock_context: MockContext, lang: str, content: list[str], expected: str, special_user: bool = False
):
    await mock_context.prepare_context(lang)
    await mock_context.prepare_alias(special_user)
    response: Response = await interact.describe_alias._callback(interact, mock_context, *content)  # NOQA
    mock_context.Asserter.assert_string(response.response_string, expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.no_content)
async def test_no_content(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_describe(interact, mock_context, lang=lang, content=[], expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.wrong_alias_no_description)
async def test_wrong_alias_no_description(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_describe(interact, mock_context, lang=lang, content=["Some_alias"], expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.alias_no_description)
async def test_alias_no_description(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_describe(interact, mock_context, lang=lang, content=["The_Tests_alias"], expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.alias_description)
async def test_alias_description(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_describe(
        interact, mock_context, lang=lang, content=["The_Tests_alias", "Some_description"], expected=expected
    )
