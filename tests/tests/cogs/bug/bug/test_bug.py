import pytest
import pytest_asyncio

from bot.cogs.bug.command.bug import Bug, BugCmd, Response
from tests.helpers.mock_classes import MockContext

from .test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return BugCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang, interact=interact)
    mock_context.Asserter.assert_string(interact.translations.Bug.deco_usage("+"), usage, strict=True)
    mock_context.Asserter.assert_string(interact.translations.Bug.deco_helper("+"), helper, strict=True)


async def base_bug(
        interact,
        mock_context: MockContext,
        lang: str,
        content: str,
        expected: str | None = None,
        re_expected: str | None = None,
        success: bool = False
):
    await mock_context.prepare_context(lang, interact=interact)
    async with mock_context.MockBuilder.Discord.DiscordWebHook.send_discord_webhook():
        response: Response = await interact.bug._callback(interact, mock_context, content=content)  # NOQA
    mock_context.Asserter.assert_string(response.response, expected=expected, re_expected=re_expected)
    mock_context.Asserter.assert_boolean(response.success, success)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.no_content)
async def test_no_content(interact, mock_context: MockContext, lang: str, expected: str):
    await base_bug(
        interact,
        mock_context,
        lang=lang,
        content="",
        expected=expected,
        success=True
    )
    bug = await Bug.get(id=1)
    assert bug.content == ""


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.no_content)
async def test_content(interact, mock_context: MockContext, lang: str, expected: str):
    await base_bug(
        interact,
        mock_context,
        lang=lang,
        content="content",
        expected=expected,
        success=True
    )
    bug = await Bug.get(id=1)
    assert bug.content == "content"

