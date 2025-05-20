# -*- coding: utf-8 -*-

from unittest.mock import patch

import pytest
import pytest_asyncio

from bot.cogs.randomcolor.command.randomcolor import RandomColorCmd
from bot.translations import Response
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.randomcolor.randomcolor.test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return RandomColorCmd(bot=mock_bot)


async def base_randomcolor(
    interact, mock_context: MockContext, lang: str, content: str, expected: str, return_value: str | None
):
    await mock_context.prepare_context(lang)
    with patch("bot.apis.color.Color.name", return_value=return_value):
        response: Response = await interact.randomcolor._callback(self=interact, ctx=mock_context, tipo=content)  # NOQA
    assert response.response_string == expected, f"Expected {expected!r}, got: {response.response_string!r}"


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.no_tipo)
async def test_no_tipo(interact, mock_context: MockContext, lang: str, expected: str):
    await base_randomcolor(
        interact, mock_context, lang=lang, content="", expected=expected, return_value="Medium Purple"
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.hex_tipo)
async def test_hex_tipo(interact, mock_context: MockContext, lang: str, expected: str):
    await base_randomcolor(
        interact, mock_context, lang=lang, content="type:hex", expected=expected, return_value="Medium Purple"
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.hex_name_api_down)
async def test_hex_name_api_down(interact, mock_context: MockContext, lang: str, expected: str):
    await base_randomcolor(interact, mock_context, lang=lang, content="", expected=expected, return_value=None)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.rgb_name_api_down)
async def test_rgb_name_api_down(interact, mock_context: MockContext, lang: str, expected: str):
    await base_randomcolor(interact, mock_context, lang=lang, content="type:rgb", expected=expected, return_value=None)
