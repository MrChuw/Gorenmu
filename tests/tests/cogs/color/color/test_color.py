# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.color.command.color import ColorCmd
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.color.color.test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return ColorCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    decorator = mock_context.bot.TranslationManager.get_decorator(interact.color, mock_context)
    mock_context.Asserter.assert_string(decorator.usage, usage)
    mock_context.Asserter.assert_string(decorator.helper, helper)


async def base_color(
    interact, mock_context: MockContext, lang: str, content: str, expected: str = None, re_expected: str = None
):
    await mock_context.prepare_context(lang)
    response: Response = await interact.color._callback(interact, mock_context, content)  # NOQA
    mock_context.Asserter.assert_string(response.response_string, expected=expected, re_expected=re_expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.hex_color)
async def test_hex_color(interact, mock_context: MockContext, lang: str, expected: str):
    async with mock_context.MockBuilder.Color.name().Bot.fetch_user(None):
        await base_color(interact, mock_context, lang=lang, content="#FF4500", expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.valid_nick)
async def test_valid_nick(interact, mock_context: MockContext, lang: str, expected: str):
    async with mock_context.MockBuilder.Color.name().Bot.fetch_user().Bot.fetch_chatters_color():
        await base_color(interact, mock_context, lang=lang, content="@some_nick", expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.hex_name)
async def test_hex_name(interact, mock_context: MockContext, lang: str, expected: str):
    async with mock_context.MockBuilder.Color.name().Bot.fetch_user().Bot.fetch_chatters_color():
        await base_color(interact, mock_context, lang=lang, content="FF4500", expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.user_db)
async def test_user_db(interact, mock_context: MockContext, lang: str, expected: str):
    async with mock_context.MockBuilder.Color.name().Bot.fetch_user(user_id=12345).Bot.fetch_chatters_color():
        await base_color(interact, mock_context, lang=lang, content="@some_nick", expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.no_user_no_hex)
async def test_no_user_no_hex(interact, mock_context: MockContext, lang: str, expected: str):
    async with mock_context.MockBuilder.Color.name().Bot.fetch_user(None):
        await base_color(interact, mock_context, lang=lang, content="some_text", expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.user_no_color)
async def test_user_no_color(interact, mock_context: MockContext, lang: str, expected: str):
    async with mock_context.MockBuilder.Color.name().Bot.fetch_user().Bot.fetch_chatters_color(None):
        await base_color(interact, mock_context, lang=lang, content="@some_user", expected=expected)
