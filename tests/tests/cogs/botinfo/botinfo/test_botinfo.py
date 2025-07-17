# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.botinfo.command.botinfo import BotInfoCmd
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.botinfo.botinfo.test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return BotInfoCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    decorator = mock_context.bot.TranslationManager.get_decorator(interact.bot_info, mock_context)
    mock_context.Asserter.assert_string(decorator.usage, usage)
    mock_context.Asserter.assert_string(decorator.helper, helper)


async def base_botinfo(
    interact, mock_context: MockContext, lang: str, content: str, expected: str = None, re_expected: str = None
):
    await mock_context.prepare_context(lang)
    response: Response = await interact.bot_info._callback(interact, mock_context)  # NOQA
    mock_context.Asserter.assert_string(response.response_string, expected=expected, re_expected=re_expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.no_content)
async def test_bot_info(interact, mock_context: MockContext, lang: str, expected: str):
    mock_context.invoked_with = "botinfo"
    await base_botinfo(interact, mock_context, lang=lang, content="", re_expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.site)
async def test_site(interact, mock_context: MockContext, lang: str, expected: str):
    mock_context.invoked_with = "site"
    await base_botinfo(interact, mock_context, lang=lang, content="", expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.uptime)
async def test_uptime(interact, mock_context: MockContext, lang: str, expected: str):
    mock_context.invoked_with = "uptime"
    await base_botinfo(interact, mock_context, lang=lang, content="", re_expected=expected)
