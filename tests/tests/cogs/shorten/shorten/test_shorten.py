import pytest
import pytest_asyncio

from bot.cogs.shorten.command.shorten import ShortenCmd
from tests.helpers.mock_classes import MockContext

from .test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return ShortenCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    mock_context.Asserter.assert_string(interact.translations.Shorten.deco_usage(mock_context, "+"), usage, strict=True)
    mock_context.Asserter.assert_string(
        interact.translations.Shorten.deco_helper(mock_context, "+"), helper, strict=True
    )


async def base_shorten(
    interact,
    mock_context: MockContext,
    lang: str,
    content: str,
    expected: str | None = None,
    re_expected: str | None = None,
    success: bool = False,
):
    await mock_context.prepare_context(lang)
    response = await interact.shorten._callback(interact, mock_context, content=content)  # NOQA
    mock_context.Asserter.assert_string(response.response_string, expected=expected, re_expected=re_expected)
    mock_context.Asserter.assert_boolean(response.success, success)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.one_link)
async def test_one_link(interact, mock_context: MockContext, lang: str, expected: str):
    session = interact.SessionsCaches.Shorten.session
    async with mock_context.MockBuilder.Session.post_json(session, Params.json_success):
        await base_shorten(
            interact, mock_context, lang=lang, content="https://someurl.org/url", expected=expected, success=True
        )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.multiple_links)
async def test_multiple_links(interact, mock_context: MockContext, lang: str, expected: str):
    session = interact.SessionsCaches.Shorten.session
    async with mock_context.MockBuilder.Session.post_json(session, Params.json_success):
        await base_shorten(
            interact,
            mock_context,
            lang=lang,
            content="https://someurl.org/url, https://someurl.org/url2, https://someurl.org/url3",
            expected=expected,
            success=True,
        )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.error_link)
async def test_error(interact, mock_context: MockContext, lang: str, expected: str):
    session = interact.SessionsCaches.Shorten.session
    async with mock_context.MockBuilder.Session.post_json(session, Params.json_error).Errors.send_bug():
        await base_shorten(
            interact, mock_context, lang=lang, content="https://someurl.org/url", expected=expected, success=False
        )
