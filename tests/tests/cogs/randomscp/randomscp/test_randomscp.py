import logging

import pytest
import pytest_asyncio

from bot.cogs.randomscp.command.randomscp import RandomSCPCmd
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.randomscp.randomscp.test_params import Params


@pytest.fixture(autouse=True)
def silence_tortoise_logs():
    logging.getLogger().setLevel(logging.ERROR)


@pytest_asyncio.fixture
async def interact(mock_bot):
    return RandomSCPCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang, interact=interact)
    mock_context.Asserter.assert_string(interact.translations.RandomScp.deco_usage("+"), usage)
    mock_context.Asserter.assert_string(interact.translations.RandomScp.deco_helper("+"), helper)


async def base_randomscp(interact, mock_context: MockContext, expected, success: bool = False):
    response = await interact.randomscp._callback(interact, mock_context)  # NOQA
    mock_context.Asserter.assert_string(response.response_string, expected=expected, re_expected=None)
    mock_context.Asserter.assert_boolean(response.success, success)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.two_hundred)
async def test_two_hundred(interact, mock_context: MockContext, lang: str, expected: str):
    await mock_context.prepare_context(lang, interact=interact)
    async with mock_context.MockBuilder.Commands.get_scp("www.some_url.com"):
        await base_randomscp(interact, mock_context, expected=expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.timeout)
async def test_timeout(interact, mock_context: MockContext, lang: str, expected: str):
    await mock_context.prepare_context(lang, interact=interact)
    async with (
        mock_context.MockBuilder.Commands.get_scp(status=404)
        .Asyncio.sleep_skip()
        .Asyncio.get_event_loop_time([0, *list(range(1, 35))])
    ):
        await base_randomscp(interact, mock_context, expected=expected, success=False)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.exception)
async def test_unexpected_exception(interact, mock_context: MockContext, lang: str, expected: str, caplog):
    await mock_context.prepare_context(lang, interact=interact)

    with caplog.at_level(logging.ERROR):
        async with (
            mock_context.MockBuilder.Commands.get_scp(side_effect=Exception("fail"))
            .Bot.silence_errors()
            .Errors.send_bug()
        ):
            await base_randomscp(interact, mock_context, expected=expected, success=False)
