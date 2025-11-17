# -*- coding: utf-8 -*-

import pytest

from bot.cogs.cookies.command.cookies import CookieCmd
from bot.ext import Response
from bot.models import User
from bot.utils import Check
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.cookies.count.test_params import Params


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    mock_context.Asserter.assert_string(interact.translations.Count.deco_usage(mock_context, "+"), usage)
    mock_context.Asserter.assert_string(interact.translations.Count.deco_helper(mock_context, "+"), helper)


async def base_count(
    interact: CookieCmd,
    mock_context: MockContext,
    lang: str,
    expected: str,
    content: list,
    target_user: bool,
    success: bool = False,
):
    if content is None:
        content = []
    await mock_context.prepare_context(lang)
    await Check.cookie_check(mock_context, interact.translations)

    if target_user:
        user = await User.get_user(mock_context, translations=interact.translations, user_id=123456)
        await mock_context.create_cookie(user, received=25, consumed=54, donated=93, stocked=8534)
        response: Response = await interact.count._callback(interact, mock_context, *[user.name])  # NOQA
    else:
        await mock_context.create_cookie(user=mock_context.user, received=25, consumed=54, donated=93, stocked=8534)
        response: Response = await interact.count._callback(interact, mock_context, *content)  # NOQA

    mock_context.Asserter.assert_string(response.response_string, expected)
    mock_context.Asserter.assert_boolean(response.success, success)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.no_name)
async def test_no_name(interact, mock_context: MockContext, lang: str, expected: str):
    await base_count(interact, mock_context, target_user=False, lang=lang, content=[], expected=expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.bot_name)
async def test_bot_name(interact, mock_context: MockContext, lang: str, expected: str):
    await base_count(
        interact,
        mock_context,
        target_user=False,
        lang=lang,
        content=[mock_context.bot.bot_nick],
        expected=expected,
        success=False,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.other_user)
async def test_other_user(interact, mock_context: MockContext, lang: str, expected: str):
    await base_count(interact, mock_context, target_user=True, lang=lang, content=[], expected=expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.author_with_a_bunch_of_things)
async def test_author_with_a_bunch_of_things(interact, mock_context: MockContext, lang: str, expected: str):
    await base_count(interact, mock_context, target_user=False, lang=lang, content=[], expected=expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.user_not_found)
async def test_user_not_found(interact, mock_context: MockContext, lang: str, expected: str):
    await base_count(
        interact, mock_context, target_user=False, lang=lang, content=["random_user"], expected=expected, success=False
    )
