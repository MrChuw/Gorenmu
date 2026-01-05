import pytest
import pytest_asyncio

from bot.cogs.leave.command.leave import LeaveCmd
from bot.models import Channel, TwitchTokens
from tests.helpers.mock_classes import MockContext

from .test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return LeaveCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang, interact=interact)
    mock_context.Asserter.assert_string(interact.translations.Leave.deco_usage("+"), usage, strict=True)
    mock_context.Asserter.assert_string(interact.translations.Leave.deco_helper("+"), helper, strict=True)


async def base_leave(
    interact,
    mock_context: MockContext,
    lang: str,
    expected: str | None = None,
    re_expected: str | None = None,
    success: bool = False,
):
    await mock_context.prepare_context(lang, interact=interact)
    response: Response = await interact.leave._callback(interact, mock_context)  # NOQA
    mock_context.Asserter.assert_string(
        response.response_string, expected=expected, re_expected=re_expected, strict=True
    )
    mock_context.Asserter.assert_boolean(response.success, success)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.not_in_channel)
async def test_not_in_channel(interact, mock_context: MockContext, lang: str, expected: str):
    await base_leave(interact, mock_context, lang=lang, expected=expected, success=False)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.channel_removed)
async def test_channel_removed(interact, mock_context: MockContext, lang: str, expected: str):
    channel = await Channel.create(user_id=mock_context.user.id)
    channel.removed = True
    await channel.save()
    await base_leave(interact, mock_context, lang=lang, expected=expected, success=False)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.on_channel)
async def test_on_channel(interact, mock_context: MockContext, lang: str, expected: str):
    await Channel.create(user_id=mock_context.user.id)
    await TwitchTokens.create(user_id=mock_context.user.id)
    async with (
        mock_context.MockBuilder.Bot.delete_eventsub_subscription().Handlers.TwitchTokens.get_event_sub_subscriptions()
    ):
        await base_leave(interact, mock_context, lang=lang, expected=expected, success=True)
