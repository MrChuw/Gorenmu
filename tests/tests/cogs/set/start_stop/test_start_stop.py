import pytest
import pytest_asyncio

from bot.cogs.set.command.set import SetCmd
from tests.helpers.mock_classes import MockContext

from .test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return SetCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang, interact=interact)
    mock_context.Asserter.assert_string(interact.translations.StartStop.deco_usage("+"), usage, strict=True)
    mock_context.Asserter.assert_string(interact.translations.StartStop.deco_helper("+"), helper, strict=True)


async def base_start(
    interact,
    mock_context: MockContext,
    lang: str,
    success: bool = False,
):
    await mock_context.prepare_context(lang, interact=interact)
    response = await interact.set_start_stop._callback(interact, mock_context)  # NOQA
    mock_context.Asserter.assert_boolean(response.success, success)
    return response


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.started)
async def test_go_online(interact, mock_context: MockContext, lang: str, expected: str):
    channel = mock_context.bot.channels[mock_context.channel.name.lower()]
    channel.online = False
    mock_context.invoked_with = "set start"
    response = await base_start(interact, mock_context, lang=lang, success=True)
    mock_context.Asserter.assert_string(response.response_string, expected=expected)
    assert channel.online


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.already_on)
async def test_already_on(interact, mock_context: MockContext, lang: str, expected: str):
    channel = mock_context.bot.channels[mock_context.channel.name.lower()]
    mock_context.invoked_with = "set start"
    response = await base_start(interact, mock_context, lang=lang, success=False)
    mock_context.Asserter.assert_string(response.response_string, expected=expected)
    assert channel.online


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.stopped)
async def test_stopped(interact, mock_context: MockContext, lang: str, expected: str):
    channel = mock_context.bot.channels[mock_context.channel.name.lower()]
    mock_context.invoked_with = "set stop"
    response = await base_start(interact, mock_context, lang=lang, success=True)
    mock_context.Asserter.assert_string(response.response_string, expected=expected)
    assert not channel.online


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.already_off)
async def test_already_off(interact, mock_context: MockContext, lang: str, expected: str):
    channel = mock_context.bot.channels[mock_context.channel.name.lower()]
    channel.online = False
    mock_context.invoked_with = "set stop"
    response = await base_start(interact, mock_context, lang=lang, success=False)
    mock_context.Asserter.assert_string(response.response_string, expected=expected)
    assert not channel.online
