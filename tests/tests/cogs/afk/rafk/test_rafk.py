from datetime import datetime

import pytest
import pytest_asyncio

from bot.cogs.afk.commands.rafk import RAfkCmd
from bot.ext import Response
from bot.models import Status
from bot.types.named_tuples import RAfkNamedTuple
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.afk.rafk.test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return RAfkCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    mock_context.Asserter.assert_string(interact.translations.RAFK.deco_usage(mock_context, "+"), usage)
    mock_context.Asserter.assert_string(interact.translations.RAFK.deco_helper(mock_context, "+"), helper)


async def base_rafk(
    interact,
    mock_context: MockContext,
    lang: str,
    content: str,
    expected: str,
    time=True,
    success: bool = False,
):
    await mock_context.prepare_context(lang)
    if time:
        afk = (await Status.get_or_create(user=mock_context.user))[0]
        afk_str = RAfkNamedTuple(
            content=content,
            updated_at=datetime.strptime("2025-01-01 06:00", "%Y-%m-%d %H:%M"),
            alias="afk",
            afk=afk,
        )
        await interact.bot.memcache.RAfk.set([int(mock_context.author.id), "username"], afk_str)
    response: Response = await interact.rafk._callback(self=interact, ctx=mock_context)  # NOQA
    mock_context.Asserter.assert_string(response.response_string, expected)
    mock_context.Asserter.assert_boolean(response.success, success)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.not_in_time)
async def test_rafk_not_in_time(interact, mock_context: MockContext, lang: str, expected: str):
    await base_rafk(
        interact,
        mock_context,
        lang=lang,
        content="content",
        expected=expected,
        time=False,
        success=False,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.with_content)
async def test_rafk_with_content(interact, mock_context: MockContext, lang: str, expected: str):
    await base_rafk(
        interact,
        mock_context,
        lang=lang,
        content="content",
        expected=expected,
        success=True,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.no_content)
async def test_rafk_no_content(interact, mock_context: MockContext, lang: str, expected: str):
    await base_rafk(interact, mock_context, lang=lang, content="", expected=expected, success=True)
