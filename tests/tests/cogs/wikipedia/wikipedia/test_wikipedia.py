# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.wikipedia.command.wikipedia import WikipediaCmd
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.wikipedia.wikipedia.test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return WikipediaCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    mock_context.Asserter.assert_string(interact.translations.Wikipedia.deco_usage(mock_context, "+"), usage)
    mock_context.Asserter.assert_string(interact.translations.Wikipedia.deco_helper(mock_context, "+"), helper)


async def base_wikipedia(interact, mock_context: MockContext, expected, success: bool = False):
    response = await interact.wikipedia._callback(interact, mock_context)  # NOQA
    mock_context.Asserter.assert_string(response.response_string, expected=expected, re_expected=None)
    mock_context.Asserter.assert_boolean(response.success, success)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.two_hundred)
async def test_two_hundred(interact, mock_context: MockContext, lang: str, expected: str):
    session = interact.SessionsCaches.WikipediaCachedSession
    await mock_context.prepare_context(lang)
    async with mock_context.MockBuilder.Session.get_not_cached(session, "www.some_url.com"):
        await base_wikipedia(interact, mock_context, expected=expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.timeout)
async def test_timeout(interact, mock_context: MockContext, lang: str, expected: str):
    session = interact.SessionsCaches.WikipediaCachedSession
    await mock_context.prepare_context(lang)
    async with (
        mock_context.MockBuilder.Session.get_not_cached(session, status=404)
        .Asyncio.sleep()
        .Asyncio.get_event_loop_time([0] + list(range(1, 35)))
    ):
        await base_wikipedia(interact, mock_context, expected=expected, success=False)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.exception)
async def test_unexpected_exception(interact, mock_context: MockContext, lang: str, expected: str):
    session = interact.SessionsCaches.WikipediaCachedSession
    await mock_context.prepare_context(lang)
    async with mock_context.MockBuilder.Session.get_not_cached(
        session, side_effect=Exception("fail")
    ).Bot.silence_errors():
        await base_wikipedia(interact, mock_context, expected=expected, success=False)
