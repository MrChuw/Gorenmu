# -*- coding: utf-8 -*-
import pytest
import pytest_asyncio

from bot.cogs.afk.commands.isafk import IsAfkCmd
from bot.translations import Response
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.afk.isafk.test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return IsAfkCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    decorator = mock_context.bot.TranslationManager.get_decorator(interact.isafk, mock_context)
    mock_context.Asserter.assert_string(decorator.usage, usage)
    mock_context.Asserter.assert_string(decorator.helper, helper)


async def base_isafk(
    interact, mock_context: MockContext, lang: str, content: str, expected: str = None, re_expected: str = None
):
    await mock_context.prepare_context(lang)
    response: Response = await interact.isafk._callback(self=interact, ctx=mock_context, content=content)  # NOQA
    mock_context.Asserter.assert_string(response.response_string, expected=expected, re_expected=re_expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.own_user)
async def test_isafk_own_user(interact, mock_context: MockContext, lang: str, expected: str):
    await base_isafk(interact, mock_context, lang=lang, content="username", expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.bot_nick)
async def test_isafk_bot_nick(interact, mock_context: MockContext, lang: str, expected: str):
    await base_isafk(interact, mock_context, lang=lang, content="bot_name", expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.no_content)
async def test_isafk_no_content(interact, mock_context: MockContext, lang: str, expected: str):
    await base_isafk(interact, mock_context, lang=lang, content="status_user_50", re_expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.content)
async def test_isafk_content(interact, mock_context: MockContext, lang: str, expected: str):
    await base_isafk(interact, mock_context, lang=lang, content="status_user_51", re_expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.user_dont_exist)
async def test_isafk_user_dont_exist(interact, mock_context: MockContext, lang: str, expected: str):
    await base_isafk(interact, mock_context, lang=lang, content="not_user_1234", expected=expected)
