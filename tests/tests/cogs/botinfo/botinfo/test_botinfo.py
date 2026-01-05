import datetime

import pytest
import pytest_asyncio

from bot.cogs.botinfo.command.botinfo import BotInfoCmd
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.botinfo.botinfo.test_params import Params


@pytest_asyncio.fixture(autouse=True)
async def lock_time(mock_context: MockContext):
    time = datetime.datetime(2025, 8, 8, 17, 5, 55, tzinfo=datetime.UTC)
    async with mock_context.MockBuilder.Default.Datetime.now(time).Default.Datetime.now_forced(time):
        yield


@pytest_asyncio.fixture
async def interact(mock_bot):
    return BotInfoCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    mock_context.Asserter.assert_string(interact.translations.BotInfo.deco_usage(mock_context, "+"), usage)
    mock_context.Asserter.assert_string(interact.translations.BotInfo.deco_helper(mock_context, "+"), helper)


async def base_botinfo(
    interact,
    mock_context: MockContext,
    lang: str,
    expected: str | None = None,
    re_expected: str | None = None,
    success: bool = False,
):
    await mock_context.prepare_context(lang)
    response: Response = await interact.bot_info._callback(interact, mock_context)  # NOQA
    mock_context.Asserter.assert_string(response.response_string, expected=expected, re_expected=re_expected)
    mock_context.Asserter.assert_boolean(response.success, success)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.no_content)
async def test_bot_info(interact, mock_context: MockContext, lang: str, expected: str):
    mock_context.invoked_with = "botinfo"
    await base_botinfo(
        interact,
        mock_context,
        lang=lang,
        re_expected=expected,
        success=True,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.site)
async def test_site(interact, mock_context: MockContext, lang: str, expected: str):
    mock_context.invoked_with = "site"
    await base_botinfo(interact, mock_context, lang=lang, expected=expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.uptime)
async def test_uptime(interact, mock_context: MockContext, lang: str, expected: str):
    mock_context.invoked_with = "uptime"
    await base_botinfo(
        interact,
        mock_context,
        lang=lang,
        expected=expected,
        success=True,
    )
