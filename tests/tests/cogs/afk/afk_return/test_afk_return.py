# -*- coding: utf-8 -*-
from datetime import UTC, datetime

import pytest
import pytest_asyncio

from bot.cogs.afk.commands.afk import AFKCmd
from bot.cogs.afk.manual_event_message.afk_return import event_message
from bot.models import Status
from bot.translations import Response
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.afk.afk_return.test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return AFKCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.not_afk)
async def test_not_afk(interact, mock_context: MockContext, lang: str, expected: bool):
    await mock_context.prepare_context(lang)
    response: Response | bool = await event_message(ctx=mock_context)
    mock_context.Asserter.assert_boolean(response, expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.no_content)
async def test_no_content(interact, mock_context: MockContext, lang: str, expected: str):
    await mock_context.prepare_context(lang)
    afk = (await Status.get_or_create(user=mock_context.user))[0]
    afk.updated_at = datetime.now(UTC)
    afk.alias = "afk"
    afk.online = False
    await afk.save()
    response: Response = await event_message(ctx=mock_context)
    mock_context.Asserter.assert_string(response.response_string, expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.afk_content)
async def test_content(interact, mock_context: MockContext, lang: str, expected: str):
    await mock_context.prepare_context(lang)
    afk = (await Status.get_or_create(user=mock_context.user))[0]
    afk.updated_at = datetime.now(UTC)
    afk.alias = "afk"
    afk.message = "content"
    afk.online = False
    await afk.save()
    response: Response = await event_message(ctx=mock_context)
    mock_context.Asserter.assert_string(response.response_string, expected)
