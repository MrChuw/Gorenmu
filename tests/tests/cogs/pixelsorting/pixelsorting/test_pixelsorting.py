# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.pixelsorting.command.pixelsorting import PixelSortCmd
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.pixelsorting.pixelsorting.test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return PixelSortCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    mock_context.Asserter.assert_string(interact.translations.PixelSorting.deco_usage(mock_context, "+"), usage)
    mock_context.Asserter.assert_string(interact.translations.PixelSorting.deco_helper(mock_context, "+"), helper)


# To lazy to make those tests.
# async def base_(
#     interact, mock_context: MockContext, lang: str, content: str, expected: str = None, re_expected: str = None
# ):
#     await mock_context.prepare_context(lang)
#     response: Response = await interact.nada._callback(interact, mock_context, content)  # NOQA
#     mock_context.Asserter.assert_string(response.response_string, expected=expected, re_expected=re_expected)
#
#
# @pytest.mark.asyncio
# @pytest.mark.parametrize("lang, expected", Params.no_content)
# async def test_(interact, mock_context: MockContext, lang: str, expected: str):
#     await base_(
#         interact,
#         mock_context,
#         lang=lang,
#         content="",
#         expected=expected,
#     )
#
#
# @pytest.mark.asyncio
# @pytest.mark.parametrize("lang, expected", Params.no_content)
# async def test_(interact, mock_context: MockContext, lang: str, expected: str):
#     await base_(
#         interact,
#         mock_context,
#         lang=lang,
#         content="",
#         expected=expected,
#     )
