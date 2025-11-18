# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.math.command.math import MathCmd
from tests.helpers.mock_classes import MockContext

from .test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return MathCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    mock_context.Asserter.assert_string(interact.translations.Math.deco_usage(mock_context, "+"), usage, strict=True)
    mock_context.Asserter.assert_string(interact.translations.Math.deco_helper(mock_context, "+"), helper, strict=True)


async def base_math(
    interact,
    mock_context: MockContext,
    lang: str,
    content: str,
    expected: str = None,
    re_expected: str = None,
    success: bool = False,
):
    await mock_context.prepare_context(lang)
    response: Response = await interact.math._callback(interact, mock_context, args=content)  # NOQA
    mock_context.Asserter.assert_string(response.response_string, expected=expected, re_expected=re_expected)
    mock_context.Asserter.assert_boolean(response.success, success)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.simple_formula)
async def test_simple_formula(interact, mock_context: MockContext, lang: str, expected: str):
    await base_math(interact, mock_context, lang=lang, content="1 + 1", expected=expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.not_so_simple_formula)
async def test_not_so_simple_formula(interact, mock_context: MockContext, lang: str, expected: str):
    await base_math(interact, mock_context, lang=lang, content="sqrt(523452)", expected=expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.multi_line_ish_formula)
async def test_multi_line_ish_formula(interact, mock_context: MockContext, lang: str, expected: str):
    await base_math(
        interact,
        mock_context,
        lang=lang,
        content="k = matrix(); k.subset(index(2), 6)",
        expected=expected,
        success=True,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.error)
async def test_error(interact, mock_context: MockContext, lang: str, expected: str):
    async with mock_context.MockBuilder.Errors.send_bug():
        await base_math(interact, mock_context, lang=lang, content="blablabla", expected=expected, success=False)
