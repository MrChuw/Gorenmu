# -*- coding: utf-8 -*-

import pytest

from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.set.color.test_params import Params


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    decorator = mock_context.bot.TranslationManager.get_decorator(interact.set_color, mock_context)
    mock_context.Asserter.assert_string(decorator.usage, usage)
    mock_context.Asserter.assert_string(decorator.helper, helper)


async def base_color(interact, mock_context: MockContext, lang: str, args: str, expected: str):
    await mock_context.prepare_context(lang)
    mock_context.author.color = "#abc123"  # fallback color in case of invalid input
    response = await interact.set_color._callback(self=interact, ctx=mock_context, args=args)  # NOQA
    mock_context.Asserter.assert_string(response.response_string, expected, strict=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, args, expected", Params.color_set)
async def test_color_set(interact, mock_context: MockContext, lang: str, args: str, expected: str):
    await base_color(interact, mock_context, lang, args, expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, args, expected", Params.color_set_no_hash)
async def test_color_set_no_hash(interact, mock_context: MockContext, lang: str, args: str, expected: str):
    await base_color(interact, mock_context, lang, args, expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, args, expected", Params.color_set_short_hex)
async def test_color_set_short_hex(interact, mock_context: MockContext, lang: str, args: str, expected: str):
    await base_color(interact, mock_context, lang, args, expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, args, expected", Params.color_remove)
async def test_color_remove(interact, mock_context: MockContext, lang: str, args: str, expected: str):
    await base_color(interact, mock_context, lang, args, expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, args, expected", Params.color_invalid)
async def test_color_invalid(interact, mock_context: MockContext, lang: str, args: str, expected: str):
    await base_color(interact, mock_context, lang, args, expected)
