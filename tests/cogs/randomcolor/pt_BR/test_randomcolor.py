# -*- coding: utf-8 -*-
from unittest.mock import patch

import pytest
import pytest_asyncio

from bot.cogs.randomcolor.command.randomcolor import RandomColorCmd
from bot.translations import Response
from tests.helpers.mock_classes import MockContext


@pytest_asyncio.fixture
async def interact(mock_bot):
    return RandomColorCmd(bot=mock_bot)


@pytest.fixture
def mock_context(mock_bot):
    return MockContext("username", 12345, "channelname", 123456, mock_bot)  # NOQA


@pytest.mark.asyncio
async def test_randomcolor_no_tipo(interact, mock_context: MockContext):
    await mock_context.prepare_context("pt_BR")
    with patch("bot.apis.color.Color.name", return_value="Medium Purple"):
        response: Response = await interact.randomcolor._callback(self=interact, ctx=mock_context)
    assert (
        response.response_string
        == "#C53EDF is Medium Purple. https://color.mrchuw.com.br/hex/c53edf"
    ), f"Expected HEX + Name + Link, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_randomcolor_hex_tipo(interact, mock_context: MockContext):
    await mock_context.prepare_context("pt_BR")
    with patch("bot.apis.color.Color.name", return_value="Medium Purple"):
        response: Response = await interact.randomcolor._callback(
            self=interact, ctx=mock_context, tipo="type:hex"
        )
    assert (
        response.response_string
        == "#C53EDF is Medium Purple. https://color.mrchuw.com.br/hex/c53edf"
    ), f"Expected HEX + Name + Link, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_randomcolor_hex_name_api_down(interact, mock_context: MockContext):
    await mock_context.prepare_context("pt_BR")
    with patch("bot.apis.color.Color.name", return_value=None):
        response: Response = await interact.randomcolor._callback(self=interact, ctx=mock_context)
    assert response.response_string == (
        "#C53EDF is thecolorapi.com is inaccessible. " "https://color.mrchuw.com.br/hex/c53edf"
    ), f"Expected HEX + Name + Link error, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_randomcolor_rgb_name_api_down(interact, mock_context: MockContext):
    await mock_context.prepare_context("pt_BR")
    with patch("bot.apis.color.Color.name", return_value=None):
        response: Response = await interact.randomcolor._callback(
            self=interact, ctx=mock_context, tipo="type:rgb"
        )
    assert response.response_string == (
        "#C5D714 is thecolorapi.com is inaccessible. " "https://color.mrchuw.com.br/rgb/197,215,20"
    ), f"Expected RGB + Name + Link error, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response
