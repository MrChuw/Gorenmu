# -*- coding: utf-8 -*-

import pytest

from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.set.nick.test_params import Params


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    mock_context.Asserter.assert_string(interact.translations.Nick.deco_usage(mock_context, "+"), usage)
    mock_context.Asserter.assert_string(interact.translations.Nick.deco_helper(mock_context, "+"), helper)


async def base_nick(interact, mock_context: MockContext, lang: str, args: str, expected: str, success: bool = False):
    await mock_context.prepare_context(lang)
    response = await interact.set_nick._callback(self=interact, ctx=mock_context, args=args)
    mock_context.Asserter.assert_string(response.response_string, expected, strict=True)
    mock_context.Asserter.assert_boolean(response.success, success)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, args, expected", Params.nick_set)
async def test_nick_set(interact, mock_context: MockContext, lang: str, args: str, expected: str):
    await base_nick(interact, mock_context, lang, args, expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, args, expected", Params.nick_remove)
async def test_nick_remove(interact, mock_context: MockContext, lang: str, args: str, expected: str):
    await base_nick(interact, mock_context, lang, args, expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, args, expected", Params.nick_too_long)
async def test_nick_too_long(interact, mock_context: MockContext, lang: str, args: str, expected: str):
    await base_nick(interact, mock_context, lang, args, expected, success=False)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, args, expected", Params.nick_start_punctuation)
async def test_nick_start_punctuation(interact, mock_context: MockContext, lang: str, args: str, expected: str):
    await base_nick(interact, mock_context, lang, args, expected, success=True)
