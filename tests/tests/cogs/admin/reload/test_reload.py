# -*- coding: utf-8 -*-
from unittest.mock import patch

import pytest

from bot.translations import Response
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.admin.reload.test_params import Params


async def reload_importlib_error(interact, mock_context: MockContext, lang: str, command: str, expected: str):
    with patch("importlib.import_module", side_effect=ImportError("Error")):
        await mock_context.prepare_context(lang)
        response: Response = await interact.reload._callback(self=interact, ctx=mock_context, command=command)  # NOQA
        mock_context.Asserter.assert_string(response.response_string, expected)


async def reload_commands(
    interact, mock_context: MockContext, lang: str, command: str, expected: str = None, re_expected: str = None
):
    await mock_context.prepare_context(lang)
    response: Response = await interact.reload._callback(self=interact, ctx=mock_context, command=command)  # NOQA
    mock_context.Asserter.assert_string(response.response_string, expected, re_expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    decorator = mock_context.bot.TranslationManager.get_decorator(interact.reload, mock_context)
    mock_context.Asserter.assert_string(decorator.usage, usage)
    mock_context.Asserter.assert_string(decorator.helper, helper)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.translations)
async def test_translations(interact, mock_context: MockContext, lang: str, expected: str):
    await reload_commands(interact, mock_context, lang=lang, command="translations", expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.emotes)
async def test_emotes(interact, mock_context: MockContext, lang: str, expected: str):
    await reload_commands(interact, mock_context, lang=lang, command="emotes", expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.commands)
async def test_commands(interact, mock_context: MockContext, lang: str, expected: str):
    await reload_commands(interact, mock_context, lang=lang, command="commands", expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.all)
async def test_all(interact, mock_context: MockContext, lang: str, expected: str):
    await reload_commands(interact, mock_context, lang=lang, command="all", expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.error_translations)
async def test_error_translations(interact, mock_context: MockContext, lang: str, expected: str):
    await reload_importlib_error(interact, mock_context, lang=lang, command="translations", expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.error_emotes)
async def test_error_emotes(interact, mock_context: MockContext, lang: str, expected: str):
    await reload_importlib_error(interact, mock_context, lang=lang, command="emotes", expected=expected)
