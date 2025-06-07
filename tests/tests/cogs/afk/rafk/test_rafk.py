# -*- coding: utf-8 -*-
from datetime import datetime

import pytest
import pytest_asyncio

from bot.cogs.afk.commands.rafk import RAfkCmd
from bot.ext.named_tuples import RAfkNamedTuple
from bot.models import Status
from bot.translations import Response
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.afk.rafk.test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return RAfkCmd(bot=mock_bot)


async def base_rafk(interact, mock_context: MockContext, lang: str, content: str, expected: str):
    await mock_context.prepare_context(lang)
    afk = (await Status.get_or_create(user=mock_context.user))[0]
    afk_str = RAfkNamedTuple(
        content=content, updated_at=datetime.strptime("2025-01-01 06:00", "%Y-%m-%d %H:%M"), alias="afk", afk=afk
    )
    await interact.bot.memcache.RAfk.set([int(mock_context.author.id), "username"], afk_str)
    response: Response = await interact.rafk._callback(self=interact, ctx=mock_context)  # NOQA
    assert response.response_string == expected, f"Expected {expected!r}, got: {response.response_string!r}"


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.not_in_time)
async def test_rafk_not_in_time(interact, mock_context: MockContext, lang: str, expected: str):
    await mock_context.prepare_context(lang)
    response: Response = await interact.rafk._callback(self=interact, ctx=mock_context)
    assert response.response_string == expected, f"Expected {expected!r}, got: {response.response_string!r}"


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.with_content)
async def test_rafk_with_content(interact, mock_context: MockContext, lang: str, expected: str):
    await base_rafk(interact, mock_context, lang=lang, content="content", expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.no_content)
async def test_rafk_no_content(interact, mock_context: MockContext, lang: str, expected: str):
    await base_rafk(interact, mock_context, lang=lang, content="", expected=expected)
