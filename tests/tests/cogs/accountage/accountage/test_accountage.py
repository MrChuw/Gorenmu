import datetime

import pytest
import pytest_asyncio

from bot.cogs.accountage.command.accountage import AccountAgeCmd
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.accountage.accountage.test_params import Params


@pytest_asyncio.fixture(autouse=True)
async def lock_time(mock_context: MockContext):
    time = datetime.datetime(2025, 8, 8, 17, 5, 55, tzinfo=datetime.UTC)
    async with mock_context.MockBuilder.Default.Datetime.now(time):
        yield


@pytest_asyncio.fixture
async def interact(mock_bot):
    return AccountAgeCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    decorator = interact.translations.AccountAge
    mock_context.Asserter.assert_string(decorator.deco_usage(mock_context, "+"), usage, strict=True)
    mock_context.Asserter.assert_string(decorator.deco_helper(mock_context, "+"), helper, strict=True)


async def base_accountage(
    interact,
    mock_context: MockContext,
    lang: str,
    content: str,
    expected: str | None = None,
    re_expected: str | None = None,
    success: bool = False,
):
    await mock_context.prepare_context(lang)
    response = await interact.accountage._callback(interact, mock_context, content)  # NOQA
    mock_context.Asserter.assert_string(
        response.response_string,
        expected=expected,
        re_expected=re_expected,
        strict=True,
    )
    mock_context.Asserter.assert_boolean(response.success, success)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.yourself)
async def test_yourself(interact, mock_context: MockContext, lang: str, expected: str):
    async with mock_context.MockBuilder.Bot.fetch_user(name=mock_context.user.name, created_at=Params._created_at):
        await base_accountage(
            interact,
            mock_context,
            lang=lang,
            content=mock_context.user.name,
            expected=expected,
            success=True,
        )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.other)
async def test_other(interact, mock_context: MockContext, lang: str, expected: str):
    async with mock_context.MockBuilder.Bot.fetch_user(name="@mr_chuw", created_at=Params._created_at):
        await base_accountage(
            interact,
            mock_context,
            lang=lang,
            content="mr_chuw",
            expected=expected,
            success=True,
        )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.not_found)
async def test_not_found(interact, mock_context: MockContext, lang: str, expected: str):
    async with mock_context.MockBuilder.Bot.fetch_user(name=None):
        await base_accountage(
            interact,
            mock_context,
            lang=lang,
            content="asdfasdf",
            expected=expected,
            success=False,
        )
