# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.afk.commands.afk import AFKCmd
from tests.cogs.afk.templates import templates_afk_return as templates
from tests.helpers.mock_classes import MockContext

lang = "en"


@pytest_asyncio.fixture
async def interact(mock_bot):
    return AFKCmd(bot=mock_bot)


@pytest.mark.en
@pytest.mark.asyncio
async def test_afk_return_not_afk(interact, mock_context: MockContext):
    await templates.test_afk_return_not_afk(interact, mock_context, lang=lang, expected=False)


@pytest.mark.en
@pytest.mark.asyncio
async def test_afk_return_afk_no_content(interact, mock_context: MockContext):
    await templates.test_afk_return_afk_no_content(
        interact, mock_context, lang=lang, expected="you came back 🏃⌨ (was away for "
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_afk_return_afk_content(interact, mock_context: MockContext):
    await templates.test_afk_return_afk_content(
        interact, mock_context, lang=lang, expected="you came back 🏃⌨ and left a note: content (was away for"
    )
