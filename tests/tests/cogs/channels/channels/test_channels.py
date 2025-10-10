# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.channels.command.channels import ChannelsCmd
from tests.helpers.mock_classes import MockContext

from .test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return ChannelsCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    mock_context.Asserter.assert_string(
        interact.translations.Channels.deco_usage(mock_context, "+"), usage, strict=True
    )
    mock_context.Asserter.assert_string(
        interact.translations.Channels.deco_helper(mock_context, "+"), helper, strict=True
    )


async def base_channels(
    interact,
    mock_context: MockContext,
    lang: str,
    content: str,
    expected: str = None,
    re_expected: str = None,
    success: bool = False,
):
    await mock_context.prepare_context(lang)
    response: Response = await interact.channels._callback(interact, mock_context, content)  # NOQA
    mock_context.Asserter.assert_string(
        response.response_string, expected=expected, re_expected=re_expected, strict=True
    )
    mock_context.Asserter.assert_boolean(response.success, success)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.no_content)
async def test_no_content(interact, mock_context: MockContext, lang: str, expected: str):
    await base_channels(interact, mock_context, lang=lang, content="", expected=expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.params_quantity)
async def test_quantity(interact, mock_context: MockContext, lang: str, expected: str):
    await base_channels(interact, mock_context, lang=lang, content="quantity", expected=expected, success=True)
