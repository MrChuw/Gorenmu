# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.randomcolor.command.randomcolor import RandomColorCmd
from tests.cogs.randomcolor.templates import templates
from tests.helpers.mock_classes import MockContext

lang = "pt_BR"


@pytest_asyncio.fixture
async def interact(mock_bot):
    return RandomColorCmd(bot=mock_bot)


@pytest.mark.asyncio
async def test_randomcolor_no_tipo(interact, mock_context: MockContext):
    await templates.test_randomcolor(
        interact,
        mock_context,
        lang=lang,
        content="",
        expected="#C53EDF é Medium Purple. https://color.mrchuw.com.br/hex/c53edf",
        return_value="Medium Purple",
    )


@pytest.mark.asyncio
async def test_randomcolor_hex_tipo(interact, mock_context: MockContext):
    await templates.test_randomcolor(
        interact,
        mock_context,
        lang=lang,
        content="type:hex",
        expected="#C53EDF é Medium Purple. https://color.mrchuw.com.br/hex/c53edf",
        return_value="Medium Purple",
    )


@pytest.mark.asyncio
async def test_randomcolor_hex_name_api_down(interact, mock_context: MockContext):
    await templates.test_randomcolor(
        interact,
        mock_context,
        lang=lang,
        content="",
        expected="#C53EDF é thecolorapi.com esta inacessível. https://color.mrchuw.com.br/hex/c53edf",
        return_value=None,
    )


@pytest.mark.asyncio
async def test_randomcolor_rgb_name_api_down(interact, mock_context: MockContext):
    await templates.test_randomcolor(
        interact,
        mock_context,
        lang=lang,
        content="type:rgb",
        expected="#C5D714 é thecolorapi.com esta inacessível. https://color.mrchuw.com.br/rgb/197,215,20",
        return_value=None,
    )
