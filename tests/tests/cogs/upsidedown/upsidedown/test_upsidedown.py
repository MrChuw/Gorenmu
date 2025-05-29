# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.upsidedown.command.upsidedown import UpSideDownCmd
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.upsidedown.upsidedown.test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return UpSideDownCmd(bot=mock_bot)


async def base_upsidedown(
    interact, mock_context: MockContext, lang: str, content: str, expected: str = None, re_expected: str = None
):
    await mock_context.prepare_context(lang)
    response: Response = await interact.upsidedown._callback(interact, mock_context, content=content)  # NOQA
    mock_context.assert_response(response, expected=expected, re_expected=re_expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.content)
async def test_content(interact, mock_context: MockContext, lang: str, expected: str):
    await base_upsidedown(interact, mock_context, lang=lang, content="some TExt", expected=expected)
