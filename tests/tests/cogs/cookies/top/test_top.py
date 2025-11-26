import pytest

from bot.ext import Response
from bot.models import User
from bot.utils import Check
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.cookies.top.test_params import Params


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    mock_context.Asserter.assert_string(interact.translations.Top.deco_usage(mock_context, "+"), usage)
    mock_context.Asserter.assert_string(interact.translations.Top.deco_helper(mock_context, "+"), helper)


async def base_top(
    interact,
    mock_context: MockContext,
    lang: str,
    content: list[str],
    expected: str,
    success: bool = False,
):
    await mock_context.prepare_context(lang)
    await Check.cookie_check(mock_context, interact.translations)
    user = await User.get_user(mock_context, translations=interact.translations, user_id=123456)
    await mock_context.create_cookie(user, received=25, consumed=54, donated=93, stocked=8534)
    response: Response = await interact.top._callback(interact, mock_context, *content)  # NOQA
    mock_context.Asserter.assert_string(response.response_string, expected)
    mock_context.Asserter.assert_boolean(response.success, success)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.no_content)
async def test_no_content(interact, mock_context: MockContext, lang: str, expected: str):
    await base_top(interact, mock_context, lang=lang, content=[], expected=expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.stocked)
async def test_stocked(interact, mock_context: MockContext, lang: str, expected: str):
    await base_top(
        interact,
        mock_context,
        lang=lang,
        content=["stocked"],
        expected=expected,
        success=True,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.consumed)
async def test_consumed(interact, mock_context: MockContext, lang: str, expected: str):
    await base_top(
        interact,
        mock_context,
        lang=lang,
        content=["consumed"],
        expected=expected,
        success=True,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.donated)
async def test_donated(interact, mock_context: MockContext, lang: str, expected: str):
    await base_top(
        interact,
        mock_context,
        lang=lang,
        content=["donated"],
        expected=expected,
        success=True,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.received)
async def test_received(interact, mock_context: MockContext, lang: str, expected: str):
    await base_top(
        interact,
        mock_context,
        lang=lang,
        content=["received"],
        expected=expected,
        success=True,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.total)
async def test_total(interact, mock_context: MockContext, lang: str, expected: str):
    await base_top(
        interact,
        mock_context,
        lang=lang,
        content=["total"],
        expected=expected,
        success=True,
    )
