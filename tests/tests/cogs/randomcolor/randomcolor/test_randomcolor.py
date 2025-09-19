# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.randomcolor.command.randomcolor import RandomColorCmd
from bot.translations import Response
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.randomcolor.randomcolor.test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return RandomColorCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    mock_context.Asserter.assert_string(interact.translations.RandomColor.deco_usage(mock_context, "+"), usage)
    mock_context.Asserter.assert_string(interact.translations.RandomColor.deco_helper(mock_context, "+"), helper)


async def base_randomcolor(
    interact,
    mock_context: MockContext,
    lang: str,
    content: str,
    expected: str,
    return_value: str | None,
    success: bool = False,
):
    await mock_context.prepare_context(lang)
    async with mock_context.MockBuilder.Color.name(return_value=return_value):
        response: Response = await interact.randomcolor._callback(self=interact, ctx=mock_context, tipo=content)  # NOQA
    mock_context.Asserter.assert_string(response.response_string, expected)
    mock_context.Asserter.assert_boolean(response.success, success)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.no_tipo)
async def test_no_tipo(interact, mock_context: MockContext, lang: str, expected: str):
    await base_randomcolor(
        interact, mock_context, lang=lang, content="", expected=expected, return_value="Medium Purple", success=True
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.hex_tipo)
async def test_hex_tipo(interact, mock_context: MockContext, lang: str, expected: str):
    await base_randomcolor(
        interact,
        mock_context,
        lang=lang,
        content="type:hex",
        expected=expected,
        return_value="Medium Purple",
        success=True,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.hex_name_api_down)
async def test_hex_name_api_down(interact, mock_context: MockContext, lang: str, expected: str):
    await base_randomcolor(
        interact, mock_context, lang=lang, content="", expected=expected, return_value=None, success=True
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.rgb_name_api_down)
async def test_rgb_name_api_down(interact, mock_context: MockContext, lang: str, expected: str):
    await base_randomcolor(
        interact, mock_context, lang=lang, content="type:rgb", expected=expected, return_value=None, success=True
    )
