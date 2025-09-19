# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.reverse.command.reverse import Response, ReverseCmd
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.reverse.reverse.test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return ReverseCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    mock_context.Asserter.assert_string(interact.translations.Reverse.deco_usage(mock_context, "+"), usage)
    mock_context.Asserter.assert_string(interact.translations.Reverse.deco_helper(mock_context, "+"), helper)


async def base_reverse(
    interact,
    mock_context: MockContext,
    lang: str,
    content: str,
    expected: str = None,
    re_expected: str = None,
    success: bool = False,
):
    await mock_context.prepare_context(lang)
    response: Response = await interact.reverse._callback(interact, mock_context, content=content)  # NOQA
    mock_context.Asserter.assert_string(response.response_string, expected=expected, re_expected=re_expected)
    mock_context.Asserter.assert_boolean(response.success, success)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.content)
async def test_content(interact, mock_context: MockContext, lang: str, expected: str):
    await base_reverse(interact, mock_context, lang=lang, content="blablabla", expected=expected, success=True)
