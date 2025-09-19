# -*- coding: utf-8 -*-

from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio

from bot.cogs.hypertranslate.command.hypertranslate import HyperTranslateCmd
from bot.translations import Response
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.hypertranslate.hypertranslate.test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return HyperTranslateCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    mock_context.Asserter.assert_string(interact.translations.HyperTranslate.deco_usage(mock_context, "+"), usage)
    mock_context.Asserter.assert_string(interact.translations.HyperTranslate.deco_helper(mock_context, "+"), helper)


async def base_nada(
    interact,
    mock_context: MockContext,
    lang: str,
    content: str,
    expected: str,
    quantity: int,
    pass_q: bool,
    success: bool = False,
):
    await mock_context.prepare_context(lang)
    with (
        patch("bot.apis.translate.base.GoogleTranslator.translate", return_value=AsyncMock()) as mock_google,
        patch("asyncio.sleep", new=AsyncMock()),
    ):
        mock_google.return_value = expected
        response: Response = await interact.hypertranslate._callback(  # NOQA
            interact, mock_context, quantity=str(quantity) if pass_q else content, text=content if pass_q else ""
        )
    mock_context.Asserter.assert_string(response.response_string, expected)
    mock_context.Asserter.assert_boolean(response.success, success)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.text)
async def test_text(interact, mock_context: MockContext, lang: str, expected: str):
    await base_nada(
        interact, mock_context, lang=lang, content="blabla", expected=expected, quantity=10, pass_q=False, success=True
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.text_and_quantity)
async def test_text_and_quantity(interact, mock_context: MockContext, lang: str, expected: str):
    await base_nada(
        interact,
        mock_context,
        lang=lang,
        content="blablabla",
        expected=expected,
        quantity=100,
        pass_q=True,
        success=True,
    )
