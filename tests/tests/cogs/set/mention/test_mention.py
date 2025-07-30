# -*- coding: utf-8 -*-

import pytest

from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.set.mention.test_params import Params


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    decorator = mock_context.bot.TranslationManager.get_decorator(interact.set_mention, mock_context)
    mock_context.Asserter.assert_string(decorator.usage, usage)
    mock_context.Asserter.assert_string(decorator.helper, helper)


async def base_mention(interact, mock_context: MockContext, lang: str, args: str, expected: str):
    await mock_context.prepare_context(lang)
    response = await interact.set_mention._callback(self=interact, ctx=mock_context, args=args)  # NOQA
    mock_context.Asserter.assert_string(response.response_string, expected, strict=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, args, expected", Params.valid_on)
async def test_set_mention_on(interact, mock_context: MockContext, lang: str, args: str, expected: str):
    await base_mention(interact, mock_context, lang, args, expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, args, expected", Params.valid_off)
async def test_set_mention_off(interact, mock_context: MockContext, lang: str, args: str, expected: str):
    await base_mention(interact, mock_context, lang, args, expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, args, expected", Params.invalid_input)
async def test_set_mention_invalid(interact, mock_context: MockContext, lang: str, args: str, expected: str):
    await base_mention(interact, mock_context, lang, args, expected)
