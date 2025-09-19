# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.profilepicture.command.profilepicture import ProfilePictureCmd
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.profilepicture.profilepicture.test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return ProfilePictureCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    mock_context.Asserter.assert_string(interact.translations.ProfilePicture.deco_usage(mock_context, "+"), usage)
    mock_context.Asserter.assert_string(interact.translations.ProfilePicture.deco_helper(mock_context, "+"), helper)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.success)
async def test_success(interact, mock_context: MockContext, lang, expected):
    await mock_context.prepare_context(lang)
    session = interact.SessionsCaches.ProfilePictureCachedSession.session
    async with (
        mock_context.MockBuilder.Bot.fetch_user(name="@mr_chuw")
        .Session.get(session=session, return_value=expected)
        .Session.post_json(session=session, return_value={"url": expected})
    ):
        response = await interact.profilepicture._callback(self=interact, ctx=mock_context, name="")
        mock_context.Asserter.assert_string(response.response_string.strip(), expected, strict=True)
    mock_context.Asserter.assert_boolean(response.success, True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.not_found)
async def test_not_found(interact, mock_context: MockContext, lang, expected):
    await mock_context.prepare_context(lang)
    async with mock_context.MockBuilder.Bot.fetch_user(name=None):
        response = await interact.profilepicture._callback(self=interact, ctx=mock_context, name="unknown_user")
        mock_context.Asserter.assert_string(response.response_string, expected, strict=True)
    mock_context.Asserter.assert_boolean(response.success, False)
