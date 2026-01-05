import datetime

import pytest
import pytest_asyncio

from bot.cogs.preview.command.preview import PreviewCmd
from tests.helpers.mock_classes import MockContext

from .test_params import Params


@pytest_asyncio.fixture(autouse=True)
async def lock_time(mock_context: MockContext):
    time = datetime.datetime(2025, 8, 8, 17, 5, 55, tzinfo=datetime.UTC)
    async with mock_context.MockBuilder.Default.Datetime.now(time):
        yield


@pytest_asyncio.fixture
async def interact(mock_bot):
    return PreviewCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    mock_context.Asserter.assert_string(interact.translations.Preview.deco_usage(mock_context, "+"), usage, strict=True)
    mock_context.Asserter.assert_string(
        interact.translations.Preview.deco_helper(mock_context, "+"),
        helper,
        strict=True,
    )


async def base_preview(
    interact,
    mock_context: MockContext,
    lang: str,
    content: str,
    expected: str | None = None,
    re_expected: str | None = None,
    success: bool = False,
):
    await mock_context.prepare_context(lang)
    response: Response = await interact.preview._callback(interact, mock_context, name=content)  # NOQA
    mock_context.Asserter.assert_string(response.response_string, expected=expected, re_expected=re_expected)
    mock_context.Asserter.assert_boolean(response.success, success)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.offline)
async def test_offline(interact, mock_context: MockContext, lang: str, expected: str):
    async with (
        mock_context.MockBuilder.ApiIvrFi.Twitch.User.fetch_user(dict_to_parse=Params.offline_json)
        .Bot.fetch_videos()
        .Bot.fetch_user()
        .Commands.get_preview()
    ):
        await base_preview(
            interact,
            mock_context,
            lang=lang,
            content="channelname",
            expected=expected,
            success=True,
        )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.online)
async def test_online(interact, mock_context: MockContext, lang: str, expected: str):
    async with (
        mock_context.MockBuilder.ApiIvrFi.Twitch.User.fetch_user(dict_to_parse=Params.online_json)
        .Bot.fetch_videos()
        .Bot.fetch_user()
        .Commands.get_preview("link")
    ):
        await base_preview(
            interact,
            mock_context,
            lang=lang,
            content="channelname",
            expected=expected,
            success=True,
        )
