# -*- coding: utf-8 -*-

import random
import string

import pytest
import pytest_asyncio

from bot.cogs.count.command.count import CountCmd
from bot.translations import Response
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.count.count.test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return CountCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    mock_context.Asserter.assert_string(interact.translations.Count.deco_usage(mock_context, "+"), usage)
    mock_context.Asserter.assert_string(interact.translations.Count.deco_helper(mock_context, "+"), helper)


async def base_count(
    interact, mock_context: MockContext, lang: str, content: str, expected, size=500, success: bool = False
):
    await mock_context.prepare_context(lang)
    random.seed(2)
    text = "".join(random.choices(f"{string.printable}©®€¥µ±§¶†‡∞∑∆∏ΩæÆßøØ¿¡†•√π÷×≠≈😊", k=size))
    session = interact.SessionsCaches.CountCachedSession.session
    async with mock_context.MockBuilder.Session.get(session, text):
        response: Response = await interact.count._callback(interact, mock_context, content=content)  # NOQA
    mock_context.Asserter.assert_string(response.response_string, expected)
    mock_context.Asserter.assert_boolean(response.success, success)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.no_content)
async def test_no_content(interact, mock_context: MockContext, lang: str, expected: str):
    await base_count(interact, mock_context, lang=lang, content="", expected=expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.some_text)
async def test_some_text(interact, mock_context: MockContext, lang: str, expected: str):
    await base_count(interact, mock_context, lang=lang, content="some text _", expected=expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.complex_text)
async def test_complex_text(interact, mock_context: MockContext, lang: str, expected: str):
    random.seed(0)
    text = "".join(random.choices(f"{string.printable}©®€¥µ±§¶†‡∞∑∆∏ΩæÆßøØ¿¡†•√π÷×≠≈😊", k=500))
    await base_count(interact, mock_context, lang=lang, content=text, expected=expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.small_site_one_url)
async def test_small_site_one_url(interact, mock_context: MockContext, lang: str, expected: str):
    await base_count(
        interact, mock_context, lang=lang, content="http://somesite.com type:url", expected=expected, success=True
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.big_site_one_url)
async def test_big_site_one_url(interact, mock_context: MockContext, lang: str, expected: str):
    await base_count(
        interact,
        mock_context,
        lang=lang,
        content="http://somesite.com type:url",
        expected=expected,
        size=100_000,
        success=True,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.small_site_four_url)
async def test_small_site_four_url(interact, mock_context: MockContext, lang: str, expected: str):
    await base_count(
        interact,
        mock_context,
        lang=lang,
        content="http://somesite1.com http://somesite2.com http://somesite3.com http://somesite4.com type:url",
        expected=expected,
        success=True,
    )
