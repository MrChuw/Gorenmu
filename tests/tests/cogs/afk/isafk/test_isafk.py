import datetime

import pytest
import pytest_asyncio

from bot.cogs.afk.commands.isafk import IsAfkCmd
from bot.ext import Response
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.afk.isafk.test_params import Params


@pytest_asyncio.fixture(autouse=True)
async def lock_time(mock_context: MockContext):
    time = datetime.datetime(2025, 8, 8, 17, 5, 55, tzinfo=datetime.UTC)
    async with mock_context.MockBuilder.Default.Datetime.now(time):
        yield


@pytest_asyncio.fixture
async def interact(mock_bot):
    return IsAfkCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang, interact=interact)
    mock_context.Asserter.assert_string(interact.translations.IsAFK.deco_usage(mock_context, "+"), usage)
    mock_context.Asserter.assert_string(interact.translations.IsAFK.deco_helper(mock_context, "+"), helper)


async def base_isafk(
    interact,
    mock_context: MockContext,
    lang: str,
    content: str,
    expected: str | None = None,
    re_expected: str | None = None,
    success: bool = False,
):
    await mock_context.prepare_context(lang, interact=interact, afk_data=True)
    response: Response = await interact.isafk._callback(self=interact, ctx=mock_context, content=content)  # NOQA
    mock_context.Asserter.assert_string(response.response_string, expected=expected, re_expected=re_expected)
    mock_context.Asserter.assert_boolean(response.success, success)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.own_user)
async def test_isafk_own_user(interact, mock_context: MockContext, lang: str, expected: str):
    await base_isafk(
        interact,
        mock_context,
        lang=lang,
        content="username",
        expected=expected,
        success=False,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.bot_nick)
async def test_isafk_bot_nick(interact, mock_context: MockContext, lang: str, expected: str):
    await base_isafk(
        interact,
        mock_context,
        lang=lang,
        content="bot_name",
        expected=expected,
        success=False,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.no_content)
async def test_isafk_no_content(interact, mock_context: MockContext, lang: str, expected: str):
    await base_isafk(
        interact,
        mock_context,
        lang=lang,
        content="status_user_50",
        expected=expected,
        success=True,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.content)
async def test_isafk_content(interact, mock_context: MockContext, lang: str, expected: str):
    await base_isafk(
        interact,
        mock_context,
        lang=lang,
        content="status_user_51",
        expected=expected,
        success=True,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.user_dont_exist)
async def test_isafk_user_dont_exist(interact, mock_context: MockContext, lang: str, expected: str):
    await base_isafk(
        interact,
        mock_context,
        lang=lang,
        content="not_user_1234",
        expected=expected,
        success=False,
    )
