import pytest
import pytest_asyncio

from bot.cogs.userid.command.userid import UserIdCmd
from tests.helpers.mock_classes import MockContext

from .test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return UserIdCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    mock_context.Asserter.assert_string(interact.translations.UserId.deco_usage(mock_context, "+"), usage, strict=True)
    mock_context.Asserter.assert_string(
        interact.translations.UserId.deco_helper(mock_context, "+"), helper, strict=True
    )


async def base_userid(
    interact,
    mock_context: MockContext,
    lang: str,
    content: str,
    expected: str | None = None,
    re_expected: str | None = None,
    success: bool = False,
):
    await mock_context.prepare_context(lang)
    response: Response = await interact.userid._callback(interact, mock_context, content)  # NOQA
    mock_context.Asserter.assert_string(
        response.response_string, expected=expected, re_expected=re_expected, strict=True
    )
    mock_context.Asserter.assert_boolean(response.success, success)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.no_content)
async def test_no_content(interact, mock_context: MockContext, lang: str, expected: str):
    async with mock_context.MockBuilder.Bot.fetch_user():
        await base_userid(interact, mock_context, lang=lang, content="", expected=expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.invalid_user)
async def test_invalid_user(interact, mock_context: MockContext, lang: str, expected: str):
    async with mock_context.MockBuilder.Bot.fetch_user_error(IndexError("error")).Errors.send_bug():
        await base_userid(interact, mock_context, lang=lang, content="some_user", expected=expected, success=False)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.invalid_id)
async def test_invalid_id(interact, mock_context: MockContext, lang: str, expected: str):
    async with mock_context.MockBuilder.Bot.fetch_user_error(IndexError("error")).Errors.send_bug():
        await base_userid(interact, mock_context, lang=lang, content="123456", expected=expected, success=False)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.no_user)
async def test_no_user(interact, mock_context: MockContext, lang: str, expected: str):
    async with mock_context.MockBuilder.Bot.fetch_user(name=None):
        await base_userid(interact, mock_context, lang=lang, content="some_user", expected=expected, success=False)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.no_id)
async def test_no_id(interact, mock_context: MockContext, lang: str, expected: str):
    async with mock_context.MockBuilder.Bot.fetch_user(name=None):
        await base_userid(interact, mock_context, lang=lang, content="123456", expected=expected, success=False)
