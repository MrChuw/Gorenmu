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


async def base_isafk(interact, mock_context: MockContext, lang: str, content: str, expected: str):
    await mock_context.prepare_context(lang)
    response: Response = await interact.isafk._callback(self=interact, ctx=mock_context, content=content)  # NOQA
    assert response.response_string == expected, f"Expected {expected!r}, got: {response.response_string!r}"


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
    await base_isafk(interact, mock_context, lang=lang, content="status_user_50", expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.content)
async def test_isafk_content(interact, mock_context: MockContext, lang: str, expected: str):
    await base_isafk(interact, mock_context, lang=lang, content="status_user_51", expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.user_dont_exist)
async def test_isafk_user_dont_exist(interact, mock_context: MockContext, lang: str, expected: str):
    await base_isafk(interact, mock_context, lang=lang, content="not_user_1234", expected=expected)
