# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.live.command.live import LiveCmd
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.live.live.test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return LiveCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    decorator = mock_context.bot.TranslationManager.get_decorator(interact.live, mock_context)
    mock_context.Asserter.assert_string(decorator.usage, usage, strict=True)
    mock_context.Asserter.assert_string(decorator.helper, helper, strict=True)


async def base_live(
    interact,
    mock_context: MockContext,
    lang: str,
    content: str,
    expected: str = None,
    re_expected: str = None,
    json_response: dict | None = None,
):
    await mock_context.prepare_context(lang)
    async with mock_context.MockBuilder.ApiIvrFi.User.fetch_user(dict_to_parse=json_response).Bot.fetch_videos():
        response = await interact.live._callback(self=interact, ctx=mock_context, channel=content)  # NOQA
        mock_context.Asserter.assert_string(response.response_string, expected=expected, re_expected=re_expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.live_on)
async def test_live_on(interact, mock_context: MockContext, lang: str, expected: str):
    await base_live(
        interact=interact,
        mock_context=mock_context,
        lang=lang,
        content="",
        re_expected=expected,
        json_response=Params.online_json,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.live_off)
async def test_live_off(interact, mock_context: MockContext, lang: str, expected: str):
    await base_live(
        interact=interact,
        mock_context=mock_context,
        lang=lang,
        content="",
        re_expected=expected,
        json_response=Params.offline_json,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.not_found)
async def test_live_user_not_found(interact, mock_context: MockContext, lang: str, expected: str):
    await base_live(
        interact=interact, mock_context=mock_context, lang=lang, content="nonexistent_user", expected=expected
    )
