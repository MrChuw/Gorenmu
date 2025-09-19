# -*- coding: utf-8 -*-

import pytest

from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.set.city.test_params import Params


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    mock_context.Asserter.assert_string(interact.translations.City.deco_usage(mock_context, "+"), usage)
    mock_context.Asserter.assert_string(interact.translations.City.deco_helper(mock_context, "+"), helper)


async def base_city(interact, mock_context: MockContext, lang: str, args: str, expected: str, success: bool = False):
    await mock_context.prepare_context(lang)
    response = await interact.set_city._callback(self=interact, ctx=mock_context, args=args)  # NOQA
    mock_context.Asserter.assert_string(response.response_string, expected, strict=True)
    mock_context.Asserter.assert_boolean(response.success, success)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, args, expected", Params.set_city_add)
async def test_set_city_add(interact, mock_context: MockContext, lang: str, args: str, expected: str):
    await base_city(interact, mock_context, lang, args, expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, args, expected", Params.set_city_add_hidden)
async def test_set_city_add_hidden(interact, mock_context: MockContext, lang: str, args: str, expected: str):
    await base_city(interact, mock_context, lang, args, expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, args, expected", Params.set_city_remove)
async def test_set_city_remove(interact, mock_context: MockContext, lang: str, args: str, expected: str):
    await base_city(interact, mock_context, lang, args, expected, success=True)
