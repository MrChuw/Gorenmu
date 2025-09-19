# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.choice.command.choice import ChoiceCmd
from bot.translations import Response
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.choice.choice.test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return ChoiceCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    mock_context.Asserter.assert_string(interact.translations.Choice.deco_usage(mock_context, "+"), usage)
    mock_context.Asserter.assert_string(interact.translations.Choice.deco_helper(mock_context, "+"), helper)


async def base_choice(
    interact, mock_context: MockContext, lang: str, content: str, expected: str, success: bool = False
):
    await mock_context.prepare_context(lang)
    response: Response = await interact.choice._callback(self=interact, ctx=mock_context, content=content)  # NOQA
    mock_context.Asserter.assert_string(response.response_string, expected)
    mock_context.Asserter.assert_boolean(response.success, success)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, content, expected", Params.choice_or)
async def test_choice_or(interact, mock_context: MockContext, lang: str, content: str, expected: str):
    await base_choice(interact, mock_context, lang=lang, content=content, expected="2", success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, content, expected", Params.space)
async def test_choice_space(interact, mock_context: MockContext, lang: str, content: str, expected: str):
    await base_choice(interact, mock_context, lang=lang, content=content, expected="2", success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, content, expected", Params.comma)
async def test_choice_comma(interact, mock_context: MockContext, lang: str, content: str, expected: str):
    await base_choice(interact, mock_context, lang=lang, content=content, expected="2", success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, content, expected", Params.mixed)
async def test_choice_mixed(interact, mock_context: MockContext, lang: str, content: str, expected: str):
    await base_choice(interact, mock_context, lang=lang, content=content, expected="4", success=True)
