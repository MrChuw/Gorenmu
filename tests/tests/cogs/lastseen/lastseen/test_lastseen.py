import datetime

import pytest
import pytest_asyncio

from bot.cogs.lastseen.command.lastseen import LastSeenCmd
from tests.helpers.mock_classes import MockContext

from .test_params import Params


@pytest_asyncio.fixture(autouse=True)
async def lock_time(mock_context: MockContext):
    time = datetime.datetime(2025, 8, 8, 17, 5, 55, tzinfo=datetime.UTC)
    updated = datetime.datetime(2025, 8, 7, 17, 5, 55, tzinfo=datetime.UTC)
    async with mock_context.MockBuilder.Default.Datetime.now(time).Db.TimestampMixin.updated_at(updated):
        yield


@pytest_asyncio.fixture
async def interact(mock_bot):
    return LastSeenCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang, interact=interact)
    mock_context.Asserter.assert_string(interact.translations.LastSeen.deco_usage("+"), usage, strict=True)
    mock_context.Asserter.assert_string(
        interact.translations.LastSeen.deco_helper("+"),
        helper,
        strict=True,
    )


async def base_lastseen(
    interact,
    mock_context: MockContext,
    lang: str,
    content: str,
    expected: str | None = None,
    re_expected: str | None = None,
    success: bool = False,
):
    await mock_context.prepare_context(lang, interact=interact)
    response: Response = await interact.lastseen._callback(interact, mock_context, args=content)  # NOQA
    mock_context.Asserter.assert_string(
        response.response_string,
        expected=expected,
        re_expected=re_expected,
        strict=True,
    )
    mock_context.Asserter.assert_boolean(response.success, success)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.bot)
async def test_lastseen_bot(interact, mock_context: MockContext, lang: str, expected: str):
    await base_lastseen(
        interact,
        mock_context,
        lang=lang,
        content="bot_name",
        expected=expected,
        success=False,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.author)
async def test_lastseen_author(interact: LastSeenCmd, mock_context: MockContext, lang: str, expected: str) -> None:
    await base_lastseen(
        interact=interact,
        mock_context=mock_context,
        lang=lang,
        content="username",
        expected=expected,
        success=False,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.not_found)
async def test_lastseen_not_found(interact: LastSeenCmd, mock_context: MockContext, lang: str, expected: str) -> None:
    await base_lastseen(
        interact=interact,
        mock_context=mock_context,
        lang=lang,
        content="nonexistent_user",
        expected=expected,
        success=False,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.not_authorized)
async def test_lastseen_not_authorized(
    interact: LastSeenCmd, mock_context: MockContext, lang: str, expected: str
) -> None:
    await base_lastseen(
        interact=interact,
        mock_context=mock_context,
        lang=lang,
        content="no_mention_user",
        expected=expected,
        success=True,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.last_seen)
async def test_lastseen_success(interact: LastSeenCmd, mock_context: MockContext, lang: str, expected: str) -> None:
    await base_lastseen(
        interact=interact,
        mock_context=mock_context,
        lang=lang,
        content="status_user_50",
        expected=expected,
        success=True,
    )
