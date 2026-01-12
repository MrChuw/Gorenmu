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
    mock_context.Asserter.assert_string(interact.translations.Banword.deco_usage("+"), usage, strict=True)
    mock_context.Asserter.assert_string(interact.translations.Banword.deco_helper("+"), helper, strict=True)


async def base_prefix(
    interact,
    mock_context: MockContext,
    lang: str,
    content: str,
    success: bool = False,
):
    await mock_context.prepare_context(lang, interact=interact)
    response = await interact.set_prefix._callback(interact, mock_context, arg=content)  # NOQA
    mock_context.Asserter.assert_boolean(response.success, success)
    return response


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.changed)
async def test_changed(interact, mock_context: MockContext, lang: str, expected: str):
    prefix = "-"
    response = await base_prefix(interact, mock_context, lang=lang, content=prefix, success=True)
    mock_context.Asserter.assert_string(response.response_string, expected=expected)
    channel = mock_context.bot.channels[mock_context.channel.name.lower()]
    assert prefix == channel.prefix


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.to_long)
async def test_to_long(interact, mock_context: MockContext, lang: str, expected: str):
    prefix = "---"
    response = await base_prefix(interact, mock_context, lang=lang, content=prefix, success=False)
    mock_context.Asserter.assert_string(response.response_string, expected=expected)
    channel = mock_context.bot.channels[mock_context.channel.name.lower()]
    assert prefix != channel.prefix
