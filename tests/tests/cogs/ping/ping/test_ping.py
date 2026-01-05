import datetime

import pytest
import pytest_asyncio

from bot.cogs.ping.command.ping import PingCmd
from tests.helpers.mock_classes import MockContext

from .test_params import Params


@pytest_asyncio.fixture(autouse=True)
async def lock_time(mock_context: MockContext):
    time = datetime.datetime(2025, 8, 8, 17, 5, 55, tzinfo=datetime.UTC)
    async with mock_context.MockBuilder.Default.Datetime.now(time):
        yield


@pytest_asyncio.fixture
async def interact(mock_bot):
    return PingCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    mock_context.Asserter.assert_string(interact.translations.Ping.deco_usage(mock_context, "+"), usage)
    mock_context.Asserter.assert_string(interact.translations.Ping.deco_helper(mock_context, "+"), helper)


async def base_ping(
    interact,
    mock_context: MockContext,
    lang: str,
    re_expected: str | None = None,
    success: bool = False,
):
    await mock_context.prepare_context(lang)
    response: Response = await interact.ping._callback(interact, mock_context)  # NOQA
    mock_context.Asserter.assert_string(response.response_string, re_expected=re_expected)
    mock_context.Asserter.assert_boolean(response.success, success)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.pong)
async def test_pong(interact, mock_context: MockContext, lang: str, expected: str):
    await base_ping(interact, mock_context, lang=lang, re_expected=expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.ping)
async def test_ping(interact, mock_context: MockContext, lang: str, expected: str):
    mock_context.invoke_by = "pong"
    await base_ping(interact, mock_context, lang=lang, re_expected=expected, success=True)
