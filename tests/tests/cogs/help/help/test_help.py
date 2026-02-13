import pytest
import pytest_asyncio

from bot.cogs.help.command.help import HelpCmd
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.help.help.test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return HelpCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang, interact=interact)
    mock_context.Asserter.assert_string(interact.translations.Help.deco_usage("+"), usage)
    mock_context.Asserter.assert_string(interact.translations.Help.deco_helper("+"), helper)


async def base_help(
    interact,
    mock_context: MockContext,
    lang: str,
    content: str,
    expected: str | None = None,
    re_expected: str | None = None,
    success: bool = False,
):
    await mock_context.prepare_context(lang, interact=interact)
    response: Response = await interact.help._callback(interact, mock_context, content=content)  # NOQA
    mock_context.Asserter.assert_string(response.response_string, expected=expected, re_expected=re_expected)
    mock_context.Asserter.assert_boolean(response.success, success)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.no_content)
async def test_no_content(interact, mock_context: MockContext, lang: str, expected: str):
    await base_help(interact, mock_context, lang=lang, content="", expected=expected, success=False)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.wrong_command)
async def test_wrong_command(interact, mock_context: MockContext, lang: str, expected: str):
    await base_help(
        interact,
        mock_context,
        lang=lang,
        content="pign",
        expected=expected,
        success=False,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.right_command)
async def test_right_command(interact, mock_context: MockContext, lang: str, expected: str):
    await base_help(
        interact,
        mock_context,
        lang=lang,
        content="ping",
        expected=expected,
        success=True,
    )
