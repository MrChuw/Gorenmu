# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.dicio.command.dicio import DicioCmd
from tests.helpers.mock_classes import MockContext

from .test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return DicioCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    mock_context.Asserter.assert_string(interact.translations.Dicio.deco_usage(mock_context, "+"), usage, strict=True)
    mock_context.Asserter.assert_string(interact.translations.Dicio.deco_helper(mock_context, "+"), helper, strict=True)


async def base_dicio(
    interact,
    mock_context: MockContext,
    lang: str,
    content: str,
    expected: str = None,
    re_expected: str = None,
    success: bool = False,
    response_get=None,
):
    if response_get is None:
        response_get = {}
    await mock_context.prepare_context(lang)
    session = interact.SessionsCaches.Dicio.session
    async with mock_context.MockBuilder.Session.get_json(session, response_get):
        response: Response = await interact.dicio._callback(interact, mock_context, content=content)  # NOQA
    mock_context.Asserter.assert_string(
        response.response_string, expected=expected, re_expected=re_expected, strict=True
    )
    mock_context.Asserter.assert_boolean(response.success, success)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.exist)
async def test_exist(interact, mock_context: MockContext, lang: str, expected: str):
    response = {"exist": True, "suggestions": ["a", "b", "c"], "stem": ["d"]}
    await base_dicio(
        interact, mock_context, lang=lang, content="word", expected=expected, success=True, response_get=response
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.not_exist)
async def test_not_exist(interact, mock_context: MockContext, lang: str, expected: str):
    response = {"exist": False, "suggestions": ["a", "b", "c"], "stem": []}
    await base_dicio(
        interact, mock_context, lang=lang, content="", expected=expected, success=True, response_get=response
    )
