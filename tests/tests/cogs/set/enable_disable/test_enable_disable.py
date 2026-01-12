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
    mock_context.Asserter.assert_string(interact.translations.Enable.deco_usage("+"), usage, strict=True)
    mock_context.Asserter.assert_string(interact.translations.Enable.deco_helper("+"), helper, strict=True)


async def base_enable(
    interact,
    mock_context: MockContext,
    lang: str,
    content: str,
    success: bool = False,
):
    await mock_context.prepare_context(lang, interact=interact)
    mock_context.invoked_with = "set enable"
    response = await interact.set_enable_disable._callback(interact, mock_context, arg=content)  # NOQA
    mock_context.Asserter.assert_boolean(response.success, success)
    return response


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.enable)
async def test_enable(interact, mock_context: MockContext, lang: str, expected: str):
    channel = mock_context.bot.channels[mock_context.channel.name.lower()]
    channel.disabled["weather"] = mock_context.author.id
    response = await base_enable(interact, mock_context, lang=lang, content="wt", success=True)
    mock_context.Asserter.assert_string(response.response_string, expected=expected)
    channel = mock_context.bot.channels[mock_context.channel.name.lower()]
    assert "weather" not in list(channel.disabled.keys())


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.enable_all)
async def test_enable_all(interact, mock_context: MockContext, lang: str, expected: str):
    channel = mock_context.bot.channels[mock_context.channel.name.lower()]
    channel.disabled["weather"] = mock_context.author.id
    response = await base_enable(interact, mock_context, lang=lang, content="all", success=True)
    mock_context.Asserter.assert_string(response.response_string, expected=expected)
    channel = mock_context.bot.channels[mock_context.channel.name.lower()]
    assert "weather" not in list(channel.disabled.keys())


async def base_disable(
    interact,
    mock_context: MockContext,
    lang: str,
    content: str,
    success: bool = False,
):
    await mock_context.prepare_context(lang, interact=interact)
    mock_context.invoked_with = "set disable"
    response = await interact.set_enable_disable._callback(interact, mock_context, arg=content)  # NOQA
    mock_context.Asserter.assert_boolean(response.success, success)
    return response


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.disable)
async def test_disable(interact, mock_context: MockContext, lang: str, expected: str):
    response = await base_disable(interact, mock_context, lang=lang, content="wt", success=True)
    mock_context.Asserter.assert_string(response.response_string, expected=expected)
    channel = mock_context.bot.channels[mock_context.channel.name.lower()]
    assert "weather" in list(channel.disabled.keys())


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.disable_all)
async def test_disable_all(interact, mock_context: MockContext, lang: str, expected: str):
    response = await base_disable(interact, mock_context, lang=lang, content="all", success=True)
    mock_context.Asserter.assert_string(response.response_string, expected=expected)
    channel = mock_context.bot.channels[mock_context.channel.name.lower()]
    assert "weather" in list(channel.disabled.keys())
