# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.randomline.command.randomline import RandomLineCmd
from bot.ext import Response
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.randomline.randomline.test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return RandomLineCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    mock_context.Asserter.assert_string(interact.translations.RandomLine.deco_usage(mock_context, "+"), usage)
    mock_context.Asserter.assert_string(interact.translations.RandomLine.deco_helper(mock_context, "+"), helper)


async def base_randomline(
    interact,
    mock_context: MockContext,
    lang: str,
    content: str,
    expected: str = None,
    re_expected: str = None,
    success: bool = False,
):
    await mock_context.prepare_context(lang)
    await mock_context.fake_messages()
    response: Response = await interact.randomline._callback(interact, mock_context, options=content)  # NOQA
    mock_context.Asserter.assert_string(response.response_string, expected=expected, re_expected=re_expected)
    mock_context.Asserter.assert_boolean(response.success, success)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.no_content)
async def test_no_content(interact, mock_context: MockContext, lang: str, expected: str):
    await base_randomline(interact, mock_context, lang=lang, content="", re_expected=expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.random_content)
async def test_random_content(interact, mock_context: MockContext, lang: str, expected: str):
    await base_randomline(interact, mock_context, lang=lang, content="blablabla", re_expected=expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.target_user)
async def test_target_user(interact, mock_context: MockContext, lang: str, expected: str):
    await base_randomline(
        interact, mock_context, lang=lang, content="user:username", re_expected=expected, success=True
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.target_channel)
async def test_target_channel(interact, mock_context: MockContext, lang: str, expected: str):
    await base_randomline(
        interact, mock_context, lang=lang, content="channel:channelname", re_expected=expected, success=True
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.target_channel_no_messages)
async def test_target_channel_no_messages(interact, mock_context: MockContext, lang: str, expected: str):
    await base_randomline(
        interact, mock_context, lang=lang, content="channel:some_user_49", re_expected=expected, success=False
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.target_user_no_messages)
async def test_target_user_no_messages(interact, mock_context: MockContext, lang: str, expected: str):
    await base_randomline(
        interact, mock_context, lang=lang, content="user:some_user_51", expected=expected, success=False
    )
