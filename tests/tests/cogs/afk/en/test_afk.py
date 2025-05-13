# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.afk.commands.afk import AFKCmd
from tests.tests.cogs.afk.templates import templates_afk as templates
from tests.helpers.mock_classes import MockContext

lang = "en"


@pytest_asyncio.fixture
async def interact(mock_bot):
    return AFKCmd(bot=mock_bot)


@pytest.mark.en
@pytest.mark.asyncio
async def test_afk_no_content(interact, mock_context: MockContext):
    await templates.test_afk_no_content(interact, mock_context, lang=lang, expected="you went afk 🏃⌨")


@pytest.mark.en
@pytest.mark.asyncio
async def test_afk_content(interact, mock_context: MockContext):
    await templates.test_afk_content(
        interact,
        mock_context,
        lang=lang,
        content="Just a test",
        expected="you went afk 🏃⌨ and left a note with: Just a test",
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_afk_too_much_content(interact, mock_context: MockContext):
    await templates.test_afk_content(
        interact,
        mock_context,
        lang=lang,
        content="a" * 500,
        expected="The message must have a maximum of 450 characters.",
    )
