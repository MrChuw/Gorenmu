import pytest
import pytest_asyncio

from bot.cogs.followage.command.followage import FollowAgeCmd
from tests.helpers.mock_classes import MockContext

from .test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return FollowAgeCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    mock_context.Asserter.assert_string(
        interact.translations.FollowAge.deco_usage(mock_context, "+"),
        usage,
        strict=True,
    )
    mock_context.Asserter.assert_string(
        interact.translations.FollowAge.deco_helper(mock_context, "+"),
        helper,
        strict=True,
    )


async def base_followage(
    interact,
    mock_context: MockContext,
    lang: str,
    content: str,
    expected: str | None = None,
    re_expected: str | None = None,
    success: bool = False,
    json_response: dict | None = None,
):
    await mock_context.prepare_context(lang)
    async with mock_context.MockBuilder.ApiIvrFi.Twitch.Channel.fetch_preview(
        dict_to_parse=json_response
    ).Bot.fetch_user("xXCoolNickXx"):
        response = await interact.followage._callback(
            interact, mock_context, name=content.split()[0], channel=content.split()[1]
        )  # NOQA
    mock_context.Asserter.assert_string(response.response_string, expected=expected, re_expected=re_expected)
    mock_context.Asserter.assert_boolean(response.success, success)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.follow)
async def test_follow(interact, mock_context: MockContext, lang: str, expected: str):
    await base_followage(
        interact,
        mock_context,
        lang=lang,
        content="xXCoolNickXx xXCoolChannelXx",
        expected=expected,
        success=True,
        json_response=Params.follow_json,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.not_follow)
async def test_not_follow(interact, mock_context: MockContext, lang: str, expected: str):
    await base_followage(
        interact,
        mock_context,
        lang=lang,
        content="xXCoolNickXx xXCoolChannelXx",
        re_expected=expected,
        success=False,
        json_response=Params.not_follow_json,
    )
